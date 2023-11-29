#!/bin/env python3

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

import os
import pyarrow
import sys

from scidbbridge import Array, type_map_pyarrow
from scidbbridge.coord import coord2delta
from scidbbridge.driver import Driver


def wrong_arg():
    print("""Upgrade an existing Bridge Array from v1 to v3.

Usage:

{} URL""".format(os.path.basename(__file__)))
    sys.exit(2)


if len(sys.argv) != 2:
    wrong_arg()

url = sys.argv[1]

for index_url in Driver.list('{}/index'.format(url)):
    print('Fixing', index_url)

    # Read index with GZIP compression
    reader = Driver.create_reader(index_url, 'gzip')
    table = reader.read_all()

    # Fix nullness in Arrow schema
    schema = pyarrow.schema([(name, pyarrow.int64(), False)
                             for name in table.schema.names])
    table = table.cast(schema)

    # Re-write index with LZ4 compression
    sink = Driver.create_writer(index_url, table.schema, 'lz4')
    writer = next(sink)
    writer.write_table(table)
    sink.close()

array = Array(url)
old_compression = array.metadata['compression']

# Change None compression to LZ4
if old_compression is None:
    array.metadata['compression'] = 'lz4'
    Driver.write_metadata(url,
                          Array.metadata_to_string(array.metadata))

# Fixed schema
schema = pyarrow.schema(
    [(a.name, type_map_pyarrow[a.type_name], not a.not_null)
     for a in array.schema.atts] +
    [('@delta', pyarrow.int64(), False)])

for (_, pos) in array.read_index().iterrows():
    chunk = array.get_chunk(*pos.tolist())
    print('Fixing', chunk.url)

    # Read chunk
    reader = Driver.create_reader(chunk.url, old_compression)
    data = reader.read_all().to_pandas()

    # Convert coordinates to delta
    data['@delta'] = coord2delta(data, array.schema.dims, chunk.coords)

    # Prepare chunk data
    table = pyarrow.Table.from_pandas(data, schema)

    # Re-write index with LZ4 compression
    sink = Driver.create_writer(chunk.url,
                                table.schema,
                                array.metadata['compression'])
    writer = next(sink)
    writer.write_table(table)
    sink.close()
