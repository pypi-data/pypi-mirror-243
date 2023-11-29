# BEGIN_COPYRIGHT
#
# Copyright (C) 2020-2023 Paradigm4 Inc.
# All Rights Reserved.
#
# scidbbridge is a plugin for SciDB, an Open Source Array DBMS
# maintained by Paradigm4. See http://www.paradigm4.com/
#
# scidbbridge is free software: you can redistribute it and/or modify
# it under the terms of the AFFERO GNU General Public License as
# published by the Free Software Foundation.
#
# scidbbridge is distributed "AS-IS" AND WITHOUT ANY WARRANTY OF ANY
# KIND, INCLUDING ANY IMPLIED WARRANTY OF MERCHANTABILITY,
# NON-INFRINGEMENT, OR FITNESS FOR A PARTICULAR PURPOSE. See the
# AFFERO GNU General Public License for the complete license terms.
#
# You should have received a copy of the AFFERO GNU General Public
# License along with scidbbridge. If not, see
# <http://www.gnu.org/licenses/agpl-3.0.html>
#
# END_COPYRIGHT

import boto3
import collections
import itertools
import os
import os.path
import numpy
import pandas
import pyarrow
import scidbpy
from typing import List

from .driver import Driver
from .coord import coord2delta, delta2coord

__version__ = '19.11.7'

type_map_pyarrow = dict(
    [(t.__str__(), t) for t in (pyarrow.binary(),
                                pyarrow.bool_(),
                                pyarrow.int16(),
                                pyarrow.int32(),
                                pyarrow.int64(),
                                pyarrow.int8(),
                                pyarrow.string(),
                                pyarrow.uint16(),
                                pyarrow.uint32(),
                                pyarrow.uint64(),
                                pyarrow.uint8())] +
    [('char', pyarrow.string()),
     ('datetime', pyarrow.timestamp('s')),
     ('double', pyarrow.float64()),
     ('float', pyarrow.float32())])


class Array(object):
    """Wrapper for SciDB array stored externally

    Constructor parameters:

    :param string url: URL of the SciDB array. Supported schemas are
      ``s3://`` and ``file://``.

    :param string schema: SciDB array schema for creating a new
      array. Can be specified as ``string`` or ``scidbpy.Schema``
    """
    # 'schema' is a class variable
    schema = None  # type: scidbpy.Schema

    def __init__(self,
                 url,
                 schema=None,
                 format='arrow',
                 compression='lz4',
                 namespace='public',
                 index_split=100000):
        self.url = url

        if schema is None:
            self._metadata = None
            self._schema = None

        else:                   # Create new array
            if type(schema) is scidbpy.Schema:
                self._schema = schema
            else:
                self._schema = scidbpy.Schema.fromstring(schema)

            self._metadata = {
                'attribute':   'ALL',
                'format':      format,
                'version':     '1',
                'schema':      self._schema.__str__(),
                'compression': None if compression == 'none' else compression,
                'index_split': index_split,
                'namespace':   namespace
            }

            Driver.init_array(url)
            Driver.write_metadata(
                url,
                Array.metadata_to_string(self._metadata.copy()))

    def __iter__(self):
        return (i for i in (self.url, ))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __repr__(self):
        return ('{}(url={!r})').format(type(self).__name__, *self)

    def __str__(self):
        return self.url

    @property
    def metadata(self):
        if self._metadata is None:
            self._metadata = Array.metadata_from_string(
                Driver.read_metadata(self.url))
        return self._metadata

    @property
    def schema(self):
        if self._schema is None:
            self._schema = scidbpy.Schema.fromstring(
                self.metadata['schema'])
        return self._schema

    def delete(self):
        # Delete metadata file first, deleting large arrays could take sometime
        Driver.delete('{}/metadata'.format(self.url))
        Driver.delete_all(self.url)

    def read_index(self):
        # Read index as Arrow Table
        tables = []
        for index_url in Driver.list('{}/index'.format(self.url)):
            tables.append(
                Driver.read_table(index_url,
                                  Driver.index_format,
                                  Driver.index_compression))

        if len(tables):
            table = pyarrow.concat_tables(tables)

            # Convert Arrow Table index to Pandas DataFrame
            index = table.to_pandas(split_blocks=True, self_destruct=True)
            # https://arrow.apache.org/docs/python/pandas.html#reducing-
            # memory-use-i
            del table
            index.sort_values(by=list(index.columns),
                              inplace=True,
                              ignore_index=True)

            return index

        return pandas.DataFrame()

    def build_index(self):
        dims = self.schema.dims
        index = pandas.DataFrame.from_records(
            map(lambda x: Array.url_to_coords(x, dims),
                Driver.list('{}/chunks'.format(self.url))),
            columns=[d.name for d in dims])
        index.sort_values(by=list(index.columns),
                          inplace=True,
                          ignore_index=True)
        return index

    def write_index(self, index, split_size=None):
        # Check for a DataFrame
        if not isinstance(index, pandas.DataFrame):
            raise Exception("Value provided as argument " +
                            "is not a Pandas DataFrame")

        # Check index columns matches array dimentions
        dim_names = [d.name for d in self.schema.dims]
        if len(index.columns) != len(dim_names):
            raise Exception(
                ("Index columns count {} does not match " +
                 "array dimensions count {}").format(len(index.columns),
                                                     len(dim_names)))

        if not (index.columns == dim_names).all():
            raise Exception(
                ("Index columns {} does not match " +
                 "array dimensions {}").format(index.columns, dim_names))

        # Check for coordinates outside chunk boundaries
        for dim in self.schema.dims:
            vals = index[dim.name]
            if any(vals < dim.low_value):
                raise Exception("Index values smaller than " +
                                "lower bound on dimension " + dim.name)
            if dim.high_value != '*' and any(vals > dim.high_value):
                raise Exception("Index values bigger than " +
                                "upper bound on dimension " + dim.name)
            if (dim.chunk_length != '*'
                    and any((vals - dim.low_value) % dim.chunk_length != 0)):
                raise Exception("Index values misaligned " +
                                "with chunk size on dimension " + dim.name)

        # Check for duplicates
        if index.duplicated().any():
            raise Exception("Duplicate entries")

        index.sort_values(by=list(index.columns),
                          inplace=True,
                          ignore_index=True)

        if split_size is None:
            split_size = int(self.metadata['index_split'])

        index_schema = pyarrow.schema(
            [(d.name, pyarrow.int64(), False) for d in self.schema.dims])
        chunk_size = split_size // len(index.columns)

        # Remove existing index
        Driver.delete_all('{}/index'.format(self.url))

        # Write new index
        i = 0
        for offset in range(0, len(index), chunk_size):
            table = pyarrow.Table.from_pandas(
                index.iloc[offset:offset + chunk_size], index_schema)
            Driver.write_table(table,
                               '{}/index/{}'.format(self.url, i),
                               index_schema,
                               Driver.index_format,
                               Driver.index_compression)
            i += 1

    def get_chunk(self, *argv):
        return Chunk(self, *argv)

    def pandas_to_chunks(self, df: pandas.DataFrame) -> List['Chunk']:
        """Returns a list of chunks containing the given DataFrame.

        Args:
            df: pandas.DataFrame contianing data to convert to chunks
        Raises:
            Exception: If columns (attributes or dimensions) do not match,
            wrong schema or duplicate rows
        """
        # Check that columns match array schema
        dims = [d.name for d in self.schema.dims]
        columns = [a.name for a in self.schema.atts] + dims
        if len(df.columns) != len(columns):
            raise Exception(
                ("Argument columns count {} do not match " +
                    "array attributes plus dimensions count {}").format(
                        len(df.columns), len(columns)))

        if sorted(list(df.columns)) != sorted(columns):
            raise Exception(
                ("Argument columns {} does not match " +
                    "array schema {}").format(df.columns, columns))

        # Use schema order
        df = df[columns]

        # Sort by dimensions
        df = df.sort_values(by=dims, ignore_index=True)

        # Check for duplicates
        if df.duplicated(subset=dims).any():
            raise Exception("Duplicate coordinates")

        # Check for coordinates outside array boundaries
        for dim in self.schema.dims:
            max_dim = df[dim.name].max()
            min_dim = df[dim.name].min()

            if dim.high_value != "*":
                if max_dim > dim.high_value:
                    raise Exception(f"Dimension {dim.name} is " +
                                    "above maximum value.")

            if dim.low_value != "*":
                if min_dim < dim.low_value:
                    raise Exception(f"Dimension {dim.name} is " +
                                    "below minimum value.")

        group_dims = []

        for dim in self.schema.dims:
            # TODO: deal with chunk_length of '*'
            df[f"@{dim.name}"] = numpy.int64(numpy.floor(
                (df[dim.name] - dim.low_value) / dim.chunk_length))
            group_dims.append(f"@{dim.name}")

        chunks = []
        grouped_df = df.groupby(group_dims)
        for c in grouped_df.groups:
            df_chunk = grouped_df.get_group(c)
            if not isinstance(c, collections.abc.Iterable):
                # one-dim
                c = (c,)
            # already have real chunk id, but that isn't what get_chunk wants!
            parts = []
            for (coord, dim) in zip(c, self.schema.dims):
                part = coord + dim.low_value
                part = part * dim.chunk_length
                parts.append(part)
            chunk = self.get_chunk(*parts)
            chunk.from_pandas(df_chunk[columns])
            chunks.append(chunk)

        return chunks

    @staticmethod
    def metadata_from_string(input):
        res = dict(ln.split('\t') for ln in input.strip().split('\n'))
        try:
            if res['compression'] == 'none':
                res['compression'] = None
        except KeyError:
            pass
        return res

    @staticmethod
    def metadata_to_string(input):
        if input['compression'] is None:
            input['compression'] = 'none'
        return '\n'.join('{}\t{}'.format(k, v)
                         for (k, v) in input.items()) + '\n'

    @staticmethod
    def coords_to_url_suffix(coords, dims):
        parts = ['c']
        for (coord, dim) in zip(coords, dims):
            if (coord < dim.low_value or
                    dim.high_value != '*' and coord > dim.high_value):
                raise Exception(
                    ('Coordinate value, {}, is outside of dimension range, '
                     '[{}:{}]').format(
                         coord, dim.low_value, dim.high_value))

            part = coord - dim.low_value
            if part % dim.chunk_length != 0:
                raise Exception(
                    ('Coordinate value, {}, is not a multiple of ' +
                     'chunk size, {}').format(
                         coord, dim.chunk_length))
            part = part // dim.chunk_length
            parts.append(part)
        return '_'.join(map(str, parts))

    @staticmethod
    def url_to_coords(url, dims):
        part = url[url.rindex('/') + 1:]
        return tuple(
            map(lambda x: int(x[0]) * x[1].chunk_length + x[1].low_value,
                zip(part.split('_')[1:], dims)))


class Chunk(object):
    """Wrapper for SciDB array chunk stored externally"""

    def __init__(self, array, *argv):
        self.array = array
        self.coords = argv

        if (len(argv) == 1 and
                type(argv[0]) is pandas.core.series.Series):
            argv = tuple(argv[0])

        dims = self.array.schema.dims
        if len(argv) != len(dims):
            raise Exception(
                ('Number of arguments, {}, does not match the number of ' +
                 'dimensions, {}. Please specify one start coordiante for ' +
                 'each dimension.').format(len(argv),
                                           len(self.array.schema.dims)))

        part = Array.coords_to_url_suffix(self.coords, dims)
        self.url = '{}/chunks/{}'.format(self.array.url, part)
        self._table = None

    def __iter__(self):
        return (i for i in (self.array, self.url))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __repr__(self):
        return ('{}(array={!r}, url={!r})').format(
            type(self).__name__, *self)

    def __str__(self):
        return self.url

    @property
    def table(self):
        if self._table is None:
            self._table = Driver.read_table(
                self.url,
                format=self.array.metadata['format'],
                compression=self.array.metadata['compression'])
        return self._table

    def to_pandas(self):
        return delta2coord(
            self.table.to_pandas(), self.array.schema, self.coords)

    def from_pandas(self, pd):
        # Check for a DataFrame
        if not isinstance(pd, pandas.DataFrame):
            raise Exception("Value provided as argument " +
                            "is not a Pandas DataFrame")

        # Check for empty DataFrame
        if pd.empty:
            raise Exception("Pandas DataFrame is empty. " +
                            "Nothing to do.")

        # Check that columns match array schema
        dims = [d.name for d in self.array.schema.dims]
        columns = [a.name for a in self.array.schema.atts] + dims
        if len(pd.columns) != len(columns):
            raise Exception(
                ("Argument columns count {} do not match " +
                 "array attributes plus dimensions count {}").format(
                     len(pd.columns), len(columns)))

        if sorted(list(pd.columns)) != sorted(columns):
            raise Exception(
                ("Argument columns {} does not match " +
                 "array schema {}").format(pd.columns, columns))

        # Use schema order
        pd = pd[columns]

        # Sort by dimensions
        pd = pd.sort_values(by=dims, ignore_index=True)

        # Check for duplicates
        if pd.duplicated(subset=dims).any():
            raise Exception("Duplicate coordinates")

        # Check for coordinates outside chunk boundaries
        for (coord, dim) in zip(self.coords, self.array.schema.dims):
            vals = pd[dim.name]
            if (vals.iloc[0] < coord or
                    vals.iloc[-1] >= coord + dim.chunk_length):
                raise Exception("Coordinates outside chunk boundaries")

        # Build schema
        schema = pyarrow.schema(
            [(a.name, type_map_pyarrow[a.type_name], not a.not_null)
             for a in self.array.schema.atts] +
            [('@delta', pyarrow.int64(), False)])

        pd['@delta'] = coord2delta(pd, self.array.schema.dims, self.coords)

        self._table = pyarrow.Table.from_pandas(pd, schema)
        self._table = self._table.replace_schema_metadata()

    def save(self):
        Driver.write_table(self._table,
                           self.url,
                           self._table.schema,
                           self.array.metadata['format'],
                           self.array.metadata['compression'])
