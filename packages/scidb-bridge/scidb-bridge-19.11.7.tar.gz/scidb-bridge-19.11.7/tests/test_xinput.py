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

import itertools
import numpy
import pandas
import pyarrow
import pytest
import requests
import scidbbridge.coord
import urllib

from conftest import *


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_one_dim_one_attr(scidb_con, chunk_size):
    url = '{}/xinput/one_dim_one_attr_{}'.format(test_url, chunk_size)
    schema = '<v:int64> [i=0:19:0:{}]'.format(chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    pandas.testing.assert_frame_equal(
        array,
        pandas.DataFrame({'i': range(20), 'v': numpy.arange(0.0, 20.0)}))


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_multi_attr(scidb_con, chunk_size):
    url = '{}/xinput/multi_attr_{}'.format(test_url, chunk_size)
    schema = '<v:int64, w:int64> [i=0:19:0:{}]'.format(chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  redimension(
    apply(
      build({}, i),
      w, v * v),
    {}),
  '{}')""".format(schema.replace(', w:int64', ''),
                  schema,
                  url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    pandas.testing.assert_frame_equal(
        array,
        pandas.DataFrame({'i': range(20),
                          'v': numpy.arange(0.0, 20.0),
                          'w': (numpy.arange(0.0, 20.0) *
                                numpy.arange(0.0, 20.0))}))


@pytest.mark.parametrize('dim_start, dim_end, chunk_size',
                         ((s, e, c)
                          for s in (-21, -13, -10)
                          for e in (10, 16, 19)
                          for c in (5, 7, 10, 20)))
def test_multi_dim(scidb_con, dim_start, dim_end, chunk_size):
    url = '{}/xinput/multi_dim_{}_{}_{}'.format(
        test_url, dim_start, dim_end, chunk_size)
    schema = '<v:int64> [i={s}:{e}:0:{c}; j=-15:14:0:{c}]'.format(
        s=dim_start, e=dim_end - 1, c=chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(dim_start, dim_end):
        for j in range(-15, 15):
            i_lst.append(i)
            j_lst.append(j)
            v_lst.append(float(i))

    pandas.testing.assert_frame_equal(array,
                                      pandas.DataFrame({'i': i_lst,
                                                        'j': j_lst,
                                                        'v': v_lst}))


@pytest.mark.parametrize(
    'type_name, is_null, type_numpy, chunk_size',
    ((t, n, p, c)
     for (t, n, p) in itertools.chain(
             ((t, n, object)
              for n in (True, False)
              for t in ('binary', 'string', 'char')),

             (('datetime', n, None)
              for n in (True, False)),

             (('bool', ) + p
              for p in ((True, object),
                        (False, bool))),

             ((t, n, tn)
              for (t, tn) in (('float', numpy.float32),
                              ('double', numpy.float64))
              for n in (True, False)),

             (('{}int{}'.format(g, s),
               n,
               numpy.dtype(
                   'float{}'.format(min(s * 2, 64)) if n
                   else '{}int{}'.format(g, s)).type)
              for g in ('', 'u')
              for s in (8, 16, 32, 64)
              for n in (True, False)))
     for c in (5, 10, 20)))
def test_type(scidb_con, type_name, is_null, type_numpy, chunk_size):
    max_val = 20
    url = '{}/xinput/type_{}_{}_{}'.format(
        test_url, type_name, is_null, chunk_size)
    schema = '<v:{} {}NULL> [i=0:{}:0:{}]'.format(
        type_name, '' if is_null else 'NOT ', max_val - 1, chunk_size)

    # Store
    if type_name == 'binary':
        que = scidb_con.input(
            schema.replace('binary NULL', 'binary NOT NULL'),
            upload_data=numpy.array([bytes([i]) for i in range(max_val)],
                                    dtype='object'))
        if is_null:
            que = que.redimension(schema)
    else:
        que = scidb_con.build(schema, '{}(i)'.format(type_name))
    que.xsave("'{}'".format(url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    if type_name in ('binary', 'char'):
        v = pandas.Series((bytes([i]) if i != 0 or type_name == 'binary'
                           else bytes()
                           for i in range(max_val)),
                          dtype=object)
    elif type_name == 'string':
        v = pandas.Series((str(i) for i in range(max_val)),
                          dtype=object)
    elif type_name.startswith('datetime'):
        if is_null:
            dtype = 'datetime64[ns]'
        else:
            dtype = 'datetime64[s]'
        v = pandas.Series((pandas.Timestamp(i * 10 ** 9)
                           for i in range(max_val)),
                          dtype=dtype)
    elif type_name == 'bool':
        if is_null:
            v = pandas.Series((bool(i) for i in range(max_val)),
                              dtype=object)
        else:
            v = pandas.Series((bool(i) for i in range(max_val)))
    else:
        v = type_numpy(range(max_val))

    pandas.testing.assert_frame_equal(
        array,
        pandas.DataFrame({'i': range(max_val), 'v': v}))


# Test for Empty Cells
@pytest.mark.parametrize('dim_start, dim_end, chunk_size',
                         ((s, e, c)
                          for s in (-13, -11, -7)
                          for e in (11, 13, 17)
                          for c in (3, 7, 11)))
def test_filter_before(scidb_con, dim_start, dim_end, chunk_size):
    url = '{}/xinput/filter_before_{}_{}_{}'.format(
        test_url, dim_start, dim_end, chunk_size)
    schema = '<v:int64> [i={s}:{e}:0:{c}; j=-11:13:0:{c}]'.format(
        s=dim_start, e=dim_end - 1, c=chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  filter(build({}, i), i % 3 = 0 and i > 7),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(dim_start, dim_end):
        for j in range(-11, 14):
            if i % 3 == 0 and i > 7:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i))

    pandas.testing.assert_frame_equal(array,
                                      pandas.DataFrame({'i': i_lst,
                                                        'j': j_lst,
                                                        'v': v_lst}))


@pytest.mark.parametrize('dim_start, dim_end, chunk_size',
                         ((s, e, c)
                          for s in (-13, -11, -7)
                          for e in (11, 13, 17)
                          for c in (3, 7, 11)))
def test_filter_after(scidb_con, dim_start, dim_end, chunk_size):
    url = '{}/xinput/filter_after_{}_{}_{}'.format(
        test_url, dim_start, dim_end, chunk_size)
    schema = '<v:int64> [i={s}:{e}:0:{c}; j=-11:13:0:{c}]'.format(
        s=dim_start, e=dim_end - 1, c=chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("""
filter(
  xinput(
    '{}'),
  i % 3 = 0 and i > 7)""".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(dim_start, dim_end):
        for j in range(-11, 14):
            if i % 3 == 0 and i > 7:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i))

    pandas.testing.assert_frame_equal(array,
                                      pandas.DataFrame({'i': i_lst,
                                                        'j': j_lst,
                                                        'v': v_lst}))


def test_nulls(scidb_con):
    url = '{}/xinput/nulls'.format(test_url)
    schema = '<v:int64> [i=0:99:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, iif(i % 2 = 0, i, missing(i))),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    i_lst = []
    v_lst = []
    for i in range(100):
        i_lst.append(i)
        if i % 2 == 0:
            v_lst.append(float(i))
        else:
            v_lst.append(numpy.nan)

    pandas.testing.assert_frame_equal(array,
                                      pandas.DataFrame({'i': i_lst,
                                                        'v': v_lst}))


def test_chunk_index(scidb_con):
    size = 300
    url = '{}/xinput/chunk_index'.format(test_url)
    schema = '<v:int64> [i=0:{}:0:5]'.format(size - 1)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    pandas.testing.assert_frame_equal(
        array,
        pandas.DataFrame({'i': range(size),
                          'v': numpy.arange(0.0, float(size))}))


# Test with Different Cache Sizes
@pytest.mark.parametrize('cache_size', (None, 4000, 3000, 0))
def test_cache(scidb_con, cache_size):
    url = '{}/xinput/cache-{}'.format(test_url, cache_size)
    schema = '<v:int64 not null, w:int64 not null> [i=0:999:0:100]'

    # Store
    scidb_con.iquery("""
xsave(
  redimension(
    filter(
      apply(
        build({}, i),
        w, i * i),
      i % 100 < 80 or i >= 800),
    {}),
  '{}')""".format(schema.replace(', w:int64 not null', ''),
                  schema,
                  url))

    # Input
    que = "xinput('{}'{})".format(
        url,
        '' if cache_size is None else ', cache_size:{}'.format(cache_size))

    if cache_size == 3000:
        with pytest.raises(requests.exceptions.HTTPError):
            array = scidb_con.iquery(que, fetch=True)
    else:
        array = scidb_con.iquery(que, fetch=True)
        array = array.sort_values(by=['i']).reset_index(drop=True)

        pandas.testing.assert_frame_equal(
            array,
            pandas.DataFrame(data=((i, i, i * i)
                                   for i in range(1000)
                                   if (i % 100 < 80 or i >= 800)),
                             columns=('i', 'v', 'w')))


# Test with Multiple Arrow Chunks per File
def test_arrow_chunk(scidb_con):
    prefix = 'xinput/arrow_chunk'
    url = '{}/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:999:0:1000]'

    # Store
    # if url.startswith('s3://'):
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Re-write one SciDB Chunk file to use multiple Arrow Chunks
    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 's3':
        s3_key = '{}/{}/chunks/c_0'.format(parts.path[1:], prefix)
        obj = s3_con.get_object(Bucket=parts.netloc, Key=s3_key)
        reader = pyarrow.RecordBatchStreamReader(
            pyarrow.input_stream(pyarrow.py_buffer(obj['Body'].read()),
                                 compression='lz4'))
    elif parts.scheme == 'file':
        fn = '{}/{}/chunks/c_0'.format(parts.path, prefix)
        reader = pyarrow.RecordBatchStreamReader(
            pyarrow.input_stream(fn, compression='lz4'))

    tbl = reader.read_all()

    if url.startswith('s3://'):
        sink = pyarrow.BufferOutputStream()
        writer = pyarrow.ipc.RecordBatchStreamWriter(sink, tbl.schema)
    elif url.startswith('file://'):
        writer = pyarrow.ipc.RecordBatchStreamWriter(fn, tbl.schema)

    batches = tbl.to_batches(max_chunksize=200)  # 1000 / 200 = 5 chunks
    writer.write_table(pyarrow.Table.from_batches(batches))
    writer.close()

    if parts.scheme == 's3':
        s3_con.put_object(Body=sink.getvalue().to_pybytes(),
                          Bucket=parts.netloc,
                          Key=s3_key)

    # Input
    que = "xinput('{}')".format(url)

    with pytest.raises(requests.exceptions.HTTPError):
        array = scidb_con.iquery(que, fetch=True)


def test_missing_index(scidb_con):
    url = '{}/xinput/missing_index'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    array_gold = pandas.DataFrame({'i': range(20), 'v': map(float, range(20))})
    pandas.testing.assert_frame_equal(array, array_gold)

    scidbbridge.driver.Driver.delete(url + '/index/0')

    # Empty Array
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    with pytest.raises(AssertionError):
        pandas.testing.assert_frame_equal(array, array_gold)
    assert len(array) == 0


def test_missing_index_big(scidb_con):
    url = '{}/xinput/missing_index_big'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1; j=0:9:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i * j),
  '{}', index_split:100)""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j, float(i * j)) for i in range(20) for j in range(10)],
        columns=('i', 'j', 'v'))
    pandas.testing.assert_frame_equal(array, array_gold)

    scidbbridge.driver.Driver.delete(url + '/index/0')

    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


def test_missing_chunks(scidb_con):
    url = '{}/xinput/missing_chunks'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    array_gold = pandas.DataFrame({'i': range(20), 'v': map(float, range(20))})
    pandas.testing.assert_frame_equal(array, array_gold)

    scidbbridge.driver.Driver.delete(url + '/chunks/c_0')

    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


def test_wrong_index(scidb_con):
    url = '{}/xinput/wrong_index'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema.replace(', w:string', ''),
                  url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(data=[(i, j, float(i * j), str(i * j))
                                        for i in range(20)
                                        for j in range(10)],
                                  columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    ar = scidbbridge.Array(url)
    index_gold = ar.read_index()
    index_url = '{}/index/0'.format(url)

    # ---
    # Add Column to Index
    index = index_gold.copy(True)
    index['k'] = index['i']
    index_table = pyarrow.Table.from_pandas(index)
    scidbbridge.driver.Driver.write_table(
        index_table, index_url, index_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Remove Column from Index
    index = index_gold.copy(True)
    index = index.drop(['j'], axis=1)
    index_table = pyarrow.Table.from_pandas(index)
    scidbbridge.driver.Driver.write_table(
        index_table, index_url, index_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Change Column to String in Index
    index = index_gold.copy(True)
    index['j'] = 'foo'
    index_table = pyarrow.Table.from_pandas(index)
    scidbbridge.driver.Driver.write_table(
        index_table, index_url, index_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Index Not Compressed
    index = index_gold.copy(True)
    index_table = pyarrow.Table.from_pandas(index)
    scidbbridge.driver.Driver.write_table(
        index_table, index_url, index_table.schema)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Write Text File as Index
    parts = urllib.parse.urlparse(index_url)
    if parts.scheme == 's3':
        bucket = parts.netloc
        key = parts.path[1:]
        scidbbridge.driver.Driver.s3_client().put_object(
            Body="foo", Bucket=bucket, Key=key)
    elif parts.scheme == 'file':
        path = os.path.join(parts.netloc, parts.path)
        with open(path, 'w') as f:
            f.write("foo")
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


@pytest.mark.parametrize('compression', (None, 'gzip', 'lz4'))
def test_wrong_chunk(scidb_con, compression):
    compression_human = compression if compression is not None else 'none'
    url = '{}/xinput/wrong_chunk/{}'.format(test_url, compression_human)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_raw = [('v', pyarrow.int64(), True),
                  ('w', pyarrow.string(), True),
                  ('@delta', pyarrow.int64(), False)]

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}', compression:'{}')""".format(schema.replace(', w:string', ''),
                                    url,
                                    compression_human))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(data=[(i, j, float(i * j), str(i * j))
                                        for i in range(20)
                                        for j in range(10)],
                                  columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    ar = scidbbridge.Array(url)
    ch = ar.get_chunk(0, 0)
    chunk_gold = ch.to_pandas()
    chunk_url = '{}/chunks/c_0_0'.format(url)

    # ---
    # Add Column to Chunk
    chunk = chunk_gold.copy(True)
    chunk['x'] = chunk['v']
    chunk['@delta'] = scidbbridge.coord.coord2delta(
        chunk, ch.array.schema.dims, ch.coords)
    schema_arrow = pyarrow.schema(
        schema_raw[:2] +
        [('x', pyarrow.int64(), True)] +
        schema_raw[2:])
    chunk_table = pyarrow.Table.from_pandas(chunk, schema_arrow)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression=compression)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Remove Column from Chunk
    chunk = chunk_gold.copy(True)
    chunk = chunk.drop(['w'], axis=1)
    chunk['@delta'] = scidbbridge.coord.coord2delta(
        chunk, ch.array.schema.dims, ch.coords)
    schema_arrow = pyarrow.schema(schema_raw[:1] + schema_raw[2:])
    chunk_table = pyarrow.Table.from_pandas(chunk, schema_arrow)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression=compression)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Change Column to String in Chunk
    chunk = chunk_gold.copy(True)
    chunk['v'] = 'foo'
    chunk['@delta'] = scidbbridge.coord.coord2delta(
        chunk, ch.array.schema.dims, ch.coords)
    schema_arrow = pyarrow.schema(
        [('v', pyarrow.string(), True)] +
        schema_raw[1:])
    chunk_table = pyarrow.Table.from_pandas(chunk, schema_arrow)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression=compression)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Chunk w/ Different Compression
    chunk = chunk_gold.copy(True)
    chunk['@delta'] = scidbbridge.coord.coord2delta(
        chunk, ch.array.schema.dims, ch.coords)
    schema_arrow = pyarrow.schema(schema_raw)
    chunk_table = pyarrow.Table.from_pandas(chunk, schema_arrow)
    not_compression = None if compression else 'gzip'
    scidbbridge.driver.Driver.write_table(chunk_table,
                                          chunk_url,
                                          chunk_table.schema,
                                          compression=not_compression)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Write Text File as Chunk
    parts = urllib.parse.urlparse(chunk_url)
    if parts.scheme == 's3':
        bucket = parts.netloc
        key = parts.path[1:]
        scidbbridge.driver.Driver.s3_client().put_object(
            Body="foo", Bucket=bucket, Key=key)
    elif parts.scheme == 'file':
        path = os.path.join(parts.netloc, parts.path)
        with open(path, 'w') as f:
            f.write("foo")
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


def test_wrong_metadata(scidb_con):
    url = '{}/xinput/wrong_metadata'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema.replace(', w:string', ''),
                  url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(data=[(i, j, float(i * j), str(i * j))
                                        for i in range(20)
                                        for j in range(10)],
                                  columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    metadata_url = url + '/metadata'
    metadata_gold = scidbbridge.driver.Driver.read_metadata(url)
    metadata_gold_dict = scidbbridge.Array.metadata_from_string(metadata_gold)
    metadata_keys = ('attribute',
                     'compression',
                     'format',
                     'index_split',
                     'namespace',
                     'schema',
                     'version')

    # ---
    # Delete Metadata
    scidbbridge.driver.Driver.delete(metadata_url)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Delete Metadata Field
    for key in metadata_keys:
        metadata = metadata_gold_dict.copy()
        del metadata[key]
        save_metadata(metadata_url, metadata_dict2text(metadata))
        with pytest.raises(requests.exceptions.HTTPError):
            scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Add Metadata Field
    metadata = metadata_gold_dict.copy()
    metadata['foo'] = 'bar'
    save_metadata(metadata_url, metadata_dict2text(metadata))
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Wrong Metadata Field Value
    for key in metadata_keys:
        metadata = metadata_gold_dict.copy()
        metadata[key] = 'foo'
        save_metadata(metadata_url, metadata_dict2text(metadata))
        if key != 'namespace':
            with pytest.raises(requests.exceptions.HTTPError):
                scidb_con.iquery("xinput('{}')".format(url), fetch=True)
        else:
            array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
            array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
            pandas.testing.assert_frame_equal(array, array_gold)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Misstyped Type in Metadata Schema Value
    metadata = metadata_gold_dict.copy()
    metadata['schema'] = metadata['schema'].replace('int64', 'unt64')
    save_metadata(metadata_url, metadata_dict2text(metadata))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Wrong Type in Metadata Schema Value
    metadata = metadata_gold_dict.copy()
    metadata['schema'] = metadata['schema'].replace('string', 'int64')
    save_metadata(metadata_url, metadata_dict2text(metadata))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Wrong Syntax in Metadata Schema Value
    metadata = metadata_gold_dict.copy()
    metadata['schema'] = metadata['schema'].replace(']', '')
    save_metadata(metadata_url, metadata_dict2text(metadata))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Write Text File as Metadata
    save_metadata(metadata_url, "foo")
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


@pytest.mark.skipif(not security_enable,
                    reason="Requires SciDB Enterprise Edition")
def test_wrong_namespace(scidb_con):
    # Setup
    scidb_con.create_user(test_user, test_password_hash)

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    url = '{}/xinput/wrong_namespace'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'

    # FS Init
    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 'file':
        fs_path = os.path.join(parts.path, 'xinput')
        if not os.path.exists(fs_path):
            os.makedirs(fs_path)

    # Store
    scidb_con2.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema.replace(', w:string', ''),
                  url))

    # Input
    array = scidb_con2.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(data=[(i, j, float(i * j), str(i * j))
                                        for i in range(20)
                                        for j in range(10)],
                                  columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    metadata_url = url + '/metadata'
    metadata_gold = scidbbridge.driver.Driver.read_metadata(url)
    metadata_gold_dict = scidbbridge.Array.metadata_from_string(metadata_gold)
    metadata_keys = ('attribute',
                     'compression',
                     'format',
                     'index_split',
                     'namespace',
                     'schema',
                     'version')

    # ---
    # Wrong Namespace in Metadata
    metadata = metadata_gold_dict.copy()
    metadata['namespace'] = 'foo'
    save_metadata(metadata_url, metadata_dict2text(metadata))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xinput('{}')".format(url), fetch=True)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con2.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Cleanup
    scidb_con.drop_user(test_user)


@pytest.mark.skipif(not test_url.startswith('file://'),
                    reason="Requires file:// URL")
def test_wrong_url(scidb_con):
    query = "xinput('{}')"

    # Invalid URL
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query.format(''))

    # Invalid URL
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query.format('file'))

    # Invalid URL
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query.format('file//'))

    # Path Empty
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query.format('file://'))

    # Path Relative
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query.format('file://foo'))


@pytest.mark.skipif(not security_enable
                    or not test_url.startswith('file://'),
                    reason="Requires SciDB Enterprise Edition and file:// URL")
def test_io_paths_list(scidb_con):
    # Setup
    scidb_con.create_user(test_user, test_password_hash)

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    parts = urllib.parse.urlparse(test_url)
    url_prefix = 'file://'
    url_postfix = '/io_paths_list'
    url1 = '{}{}{}'.format(url_prefix, parts.path, url_postfix)
    url2 = '{}/var/lib'.format(url_prefix)
    url3 = '{}/non/existing'.format(url_prefix)

    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    query = """
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{{}}')""".format(schema.replace(', w:string', ''))

    # Store
    scidb_con2.iquery(query.format(url1))

    # Input
    array = scidb_con2.iquery("xinput('{}')".format(url1), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(data=[(i, j, float(i * j), str(i * j))
                                        for i in range(20)
                                        for j in range(10)],
                                  columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    # Not Allowed
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery(query.format(url2))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xinput('{}')".format(url2), fetch=True)

    # Does Not Exist
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery(query.format(url3))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xinput('{}')".format(url3), fetch=True)

    # Cleanup
    scidb_con.drop_user(test_user)


def test_from_pandas(scidb_con):
    url = '{}/xinput/from_pandas'.format(test_url)
    schema = '<v:int64, w:int64> [i=0:19:0:10]'

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, -i),
    w, -v * 10),
  '{}')""".format(schema.replace(', w:int64', ''), url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        {'i': range(20),
         'v': map(lambda i: -float(i), range(20)),
         'w': map(lambda i: float(i * 10), range(20))})
    pandas.testing.assert_frame_equal(array, array_gold)

    # Missing Columns
    chunk = scidbbridge.Array(url).get_chunk(10)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(
            pandas.DataFrame(((i, i * 10) for i in range(10, 20)),
                             columns=list('iw')))
    assert ('do not match array attributes plus dimensions count'
            in str(ex.value))

    # Wrong Columns
    chunk = scidbbridge.Array(url).get_chunk(10)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(
            pandas.DataFrame(((i, i * 10, -i) for i in range(10, 20)),
                             columns=list('iwx')))
    assert 'does not match array schema' in str(ex.value)

    # Swapped Columns
    chunk = scidbbridge.Array(url).get_chunk(10)
    chunk.from_pandas(
        pandas.DataFrame(((i, i * 10, -i) for i in range(10, 20)),
                         columns=list('iwv')))
    chunk.save()

    # Check Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


def test_save(scidb_con):
    url = '{}/xinput/save'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    # Store
    scidb_con.iquery("xsave(build({}, i), '{}')".format(schema, url))

    # Save
    scidb_con.iquery("save(xinput('{}'), '/dev/null')".format(url))


def test_filter_read(scidb_con):
    url = '{}/xinput/filter_sparse'.format(test_url)
    schema = '<v:int64> [i=1:10:0:10; j=1:10:0:10]'

    # Store
    scidb_con.iquery("""
xsave(
  filter(build({}, i * j), v % 3 = 0),
  '{}')""".format(schema, url))

    # Input & Filter
    array = scidb_con.iquery("filter(xinput('{}'), i % 2 = 0)".format(url),
                             fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(1, 11):
        for j in range(1, 11):
            if i * j % 3 == 0 and i % 2 == 0:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i * j))

    pandas.testing.assert_frame_equal(array,
                                      pandas.DataFrame({'i': i_lst,
                                                        'j': j_lst,
                                                        'v': v_lst}))
