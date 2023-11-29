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
import pandas
import pytest
import scidbbridge

from conftest import *


def test_chunks_all(scidb_con):
    url = '{}/api/chunks_all'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data={'i': range(0, 20, 5)}))

    for i in range(0, 20, 5):
        array.get_chunk(i)
    with pytest.raises(Exception) as ex:
        array.get_chunk()
    assert "does not match the number of dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-1)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(20)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(17)
    assert "is not a multiple of chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(0, 5)
    assert "does not match the number of dimensions" in str(ex.value)


def test_chunks_holes(scidb_con):
    url = '{}/api/chunks_holes'.format(test_url)
    schema = '<v:int64> [i=-3:31:0:7]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    i < 4 or i >= 11 and i % 3 = 0),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data={'i': [-3, 11, 18, 25]}))

    for i in range(-3, 31, 7):
        array.get_chunk(i)
    with pytest.raises(Exception) as ex:
        array.get_chunk()
    assert "does not match the number of dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-5)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(35)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(17)
    assert "is not a multiple of chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(0, 5)
    assert "does not match the number of dimensions" in str(ex.value)


def test_chunks_dim_all(scidb_con):
    url = '{}/api/chunks_dim_all'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5; j=0:19:0:10]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 20, 5)
                               for j in range(0, 20, 10)),
                         columns=('i', 'j')))

    for i in range(0, 20, 5):
        for j in range(0, 20, 10):
            array.get_chunk(i, j)
    with pytest.raises(Exception) as ex:
        array.get_chunk()
    assert "does not match the number of dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(0)
    assert "does not match the number of dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-1, 0)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(5, 17)
    assert "is not a multiple of chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(5, 10, 0)
    assert "does not match the number of dimensions" in str(ex.value)


def test_chunks_dim_holes(scidb_con):
    url = '{}/api/chunks_dim_holes'.format(test_url)
    schema = '<v:int64> [i=-3:31:0:7; j=11:23:0:3]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    i < 4 and j >= 20 or i >= 11 and j < 14 and i % 3 = 0 and j % 2 = 0),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=((i, j)
                               for i in range(-3, 32, 7)
                               for j in range(11, 24, 3)
                               if i < 4 and j >= 20 or i >= 11 and j < 14),
                         columns=('i', 'j')))

    for i in range(-3, 31, 7):
        for j in range(11, 24, 3):
            array.get_chunk(i, j)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-3)
    assert "does not match the number of dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-5, 11)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(11, 26)
    assert "is outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-3, 12)
    assert "is not a multiple of chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(-3, 11, 0)
    assert "does not match the number of dimensions" in str(ex.value)


def test_update_chunk(scidb_con):
    url = '{}/api/update_chunk'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5; j=0:19:0:10]'

    # Create Array Using xsave
    scidb_con.iquery("""
xsave(
  filter(
    build({}, i * j),
    i % 3 = 0 and j % 2 = 0),
  '{}')""".format(schema, url))

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(0, 20):
        for j in range(0, 20):
            if i % 3 == 0 and j % 2 == 0:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i * j))
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst,
                          'j': j_lst,
                          'v': v_lst}))

    # Fetch Chunks List Using Python API
    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 20, 5)
                               for j in range(0, 20, 10)),
                         columns=('i', 'j')))

    # Fetch Chunk Using Python API
    chunk = array.get_chunk(0, 0)
    pd = chunk.to_pandas()
    pandas.testing.assert_frame_equal(
        pd,
        pandas.DataFrame(data=((i * j, i, j)
                               for i in range(0, 5)
                               for j in range(0, 10)
                               if i % 3 == 0 and j % 2 == 0),
                         columns=('v', 'i', 'j')))

    # Update Chunk Using Python API
    pd = pandas.concat([pd,
                        pandas.DataFrame({'v': (100, 200),
                                          'i': (4, 1),
                                          'j': (3, 3)})],
                       ignore_index=True)

    chunk.from_pandas(pd)
    chunk.save()

    # Insert duplicates
    pd_dup = pandas.concat(
        [pd,
         pandas.DataFrame({'v': 100, 'i': 4, 'j': 3}, index=[0])],
        ignore_index=True)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_dup)
    assert "Duplicate coordinates" in str(ex.value)
    pd_dup = pandas.concat(
        [pd,
         pandas.DataFrame({'v': 100, 'i': 0, 'j': 2}, index=[0])],
        ignore_index=True)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_dup)
    assert "Duplicate coordinates" in str(ex.value)

    # Insert coordinates outside chunk boundaries
    pd_out = pandas.concat(
        [pd,
         pandas.DataFrame({'v': 100, 'i': 0, 'j': -1}, index=[0])],
        ignore_index=True)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)
    assert "Coordinates outside chunk boundaries" in str(ex.value)
    pd_out = pandas.concat(
        [pd,
         pandas.DataFrame({'v': 100, 'i': 5, 'j': 0}, index=[0])],
        ignore_index=True)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)
    assert "Coordinates outside chunk boundaries" in str(ex.value)

    # Insert empty chunk
    pd_out = pandas.DataFrame()
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)
    pd_out = pandas.DataFrame({'v': (),
                               'i': (),
                               'j': ()})
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)
    assert str(ex.value).startswith('Pandas DataFrame is empty')

    # Insert chunk with missing columns
    pd_out = pandas.DataFrame({'v': (100, 200),
                               'j': (3, 3)}),
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)
    pd_out = pandas.DataFrame({'i': (4, 1),
                               'j': (3, 3)}),
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pd_out)

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(0, 20):
        for j in range(0, 20):
            if i % 3 == 0 and j % 2 == 0:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i * j))
            elif i in (1, 4) and j == 3:
                i_lst.append(i)
                j_lst.append(j)
                if i == 4:
                    v_lst.append(float(100))
                else:
                    v_lst.append(float(200))
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst,
                          'j': j_lst,
                          'v': v_lst}))


def test_update_add_chunks(scidb_con):
    url = '{}/api/update_add_chunks'.format(test_url)
    schema = '<v:int64> [i=0:49:0:5; j=0:29:0:10]'

    # Create Array Using xsave
    scidb_con.iquery("""
xsave(
  redimension(
    filter(
      build({}, i * j),
      i % 3 = 0 and j % 2 = 0),
    {}),
  '{}')""".format(schema.replace('49', '19').replace('29', '19'),
                  schema,
                  url))

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = []
    j_lst = []
    v_lst = []
    for i in range(0, 20):
        for j in range(0, 20):
            if i % 3 == 0 and j % 2 == 0:
                i_lst.append(i)
                j_lst.append(j)
                v_lst.append(float(i * j))
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst, 'j': j_lst, 'v': v_lst}))

    # Fetch Chunks List Using Python API
    array = scidbbridge.Array(url)
    chunks = array.read_index()

    chunks_list = [(i, j)
                   for i in range(0, 20, 5)
                   for j in range(0, 20, 10)]
    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=chunks_list, columns=('i', 'j')))

    # Get New Chunk, Add Data to Chunk, Add Chunk to Index
    chunk = array.get_chunk(20, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (100, ),
                                        'i': (20, ),
                                        'j': (10, )}))
    chunk.save()
    chunks = pandas.concat([chunks,
                            pandas.DataFrame({'i': (20, ), 'j': (10, )})],
                           ignore_index=True)
    array.write_index(chunks)
    chunks = array.read_index()

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst.append(20)
    j_lst.append(10)
    v_lst.append(100)
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst, 'j': j_lst, 'v': v_lst}))

    # Add Data to Chunk
    chunk = array.get_chunk(20, 10)
    pd = chunk.to_pandas()
    pd = pandas.concat([pd,
                        pandas.DataFrame({'v': (110, 120),
                                          'i': (22, 24),
                                          'j': (11, 11)})],
                       ignore_index=True)
    chunk.from_pandas(pd)
    chunk.save()

    # Fetch Chunks List Using Python API
    chunks = array.read_index()

    chunks_list.append((20, 10))
    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=chunks_list, columns=('i', 'j')))

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = i_lst + [22, 24]
    j_lst = j_lst + [11, 11]
    v_lst = v_lst + [110, 120]
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst, 'j': j_lst, 'v': v_lst}))

    # Get Two New Chunk, Add Data to Chunks, Add Chunks to Index
    chunk = array.get_chunk(40, 20)
    chunk.from_pandas(pandas.DataFrame({'v': (10, 10),
                                        'i': (42, 43),
                                        'j': (25, 25)}))
    chunk.save()

    chunk = array.get_chunk(45, 20)
    chunk.from_pandas(pandas.DataFrame({'v': (10, 10),
                                        'i': (48, 49),
                                        'j': (25, 25)}))
    chunk.save()

    chunks = array.build_index()
    array.write_index(chunks)

    # Fetch Chunks List Using Python API
    chunks = array.read_index()

    chunks_list = chunks_list + [(40, 20), (45, 20)]
    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data=chunks_list, columns=('i', 'j')))

    # Fetch Array Using xinput
    array_pd = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array_pd = array_pd.sort_values(by=['i', 'j']).reset_index(drop=True)

    i_lst = i_lst + [42, 43, 48, 49]
    j_lst = j_lst + [25] * 4
    v_lst = v_lst + [10] * 4
    pandas.testing.assert_frame_equal(
        array_pd,
        pandas.DataFrame({'i': i_lst, 'j': j_lst, 'v': v_lst}))

    # Get Chunk Errors
    with pytest.raises(Exception) as ex:
        array.get_chunk(-5, 10)
    assert "outside of dimension range" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(0, 5)
    assert "not a multiple of chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.get_chunk(25, 10, 0)
    assert "does not match the number of dimensions" in str(ex.value)

    # Add Chunks to Index Errors
    with pytest.raises(Exception) as ex:
        array.write_index([1, 2])
    assert "argument is not a Pandas DataFrame" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (25, )}))
    assert "does not match array dimensions count" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (25, ), 'k': (20, )}))
    assert "does not match array dimensions" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (25, ), 'j': (25, )}))
    assert "Index values misaligned with chunk size" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (50, ), 'j': (20, )}))
    assert "Index values bigger than upper bound" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (25, ), 'j': (30, )}))
    assert "Index values bigger than upper bound" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame(
            {'i': (40, ), 'j': (20, ), 'l': (0, )}))
    assert "does not match array dimensions count" in str(ex.value)
    with pytest.raises(Exception) as ex:
        array.write_index(pandas.DataFrame({'i': (25, 25), 'j': (20, 20)}))
    assert "Duplicate entries" in str(ex.value)


def test_update_big_index(scidb_con):
    url = '{}/api/update_big_index'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1; j=0:9:0:1]'

    # Create Array Using xsave
    scidb_con.iquery("""
xsave(
    build({}, i * j),
  '{}', index_split:100)""".format(schema, url))

    # Fetch Chunks List Using Python API
    array = scidbbridge.Array(url)
    chunks = array.read_index()

    chunks_gold = pandas.DataFrame(
        data=[(i, j) for i in range(20) for j in range(10)],
        columns=('i', 'j'))
    pandas.testing.assert_frame_equal(chunks, chunks_gold)
    assert len(list(scidbbridge.driver.Driver.list(url + '/index'))) == 4

    # Re-index with Larger Split Size
    index = array.read_index()
    array.write_index(index, split_size=200)

    # Fetch Chunks List Using Python API
    chunks = array.read_index()
    pandas.testing.assert_frame_equal(chunks, chunks_gold)
    assert len(list(scidbbridge.driver.Driver.list(url + '/index'))) == 2

    # Re-index with Extra Large Split Size
    index = array.read_index()
    array.write_index(index, split_size=10000)

    # Fetch Chunks List Using Python API
    chunks = array.read_index()
    pandas.testing.assert_frame_equal(chunks, chunks_gold)
    assert len(list(scidbbridge.driver.Driver.list(url + '/index'))) == 1

    # Re-build Index
    index_rebuild = array.build_index()
    pandas.testing.assert_frame_equal(index, index_rebuild)

    # Save Re-built Index
    array.write_index(index_rebuild, split_size=100)
    chunks = array.read_index()
    pandas.testing.assert_frame_equal(chunks, chunks_gold)
    assert len(list(scidbbridge.driver.Driver.list(url + '/index'))) == 4


def test_unbound_dimension(scidb_con):
    url = '{}/api/unbound_dimension'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    # Create Array Using xsave
    scidb_con.iquery("""
xsave(
  redimension(
    build({}, i),
    {}),
  '{}', index_split:100)""".format(schema, schema.replace('19', '*'), url))

    # Fetch Chunk
    array = scidbbridge.Array(url)
    chunk = array.get_chunk(0)

    # Rewrite Index
    chunks = array.build_index()
    array.write_index(chunks)


def test_read_empty(scidb_con):
    name = 'empty_array_{}'.format(test_id)
    url = '{}/xinput/read_{}'.format(test_url, name)
    schema = '<v:int64> [i=0:19:0:10]'

    # Create & Store
    scidb_con.iquery("create array {} {}".format(name, schema))
    scidb_con.iquery("xsave({}, '{}')".format(name, url))

    # Fetch Chunk
    array = scidbbridge.Array(url)
    assert array.url == url
    assert array.schema.__str__() == schema
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    assert len(array.read_index()) == 0

    scidb_con.iquery("remove({})".format(name))


def test_create_empty(scidb_con):
    name = 'empty_array'
    url = '{}/api/create_{}'.format(test_url, name)
    schema = '<v:int64> [i=0:19:0:10]'

    # Create
    array = scidbbridge.Array(url, schema)

    res = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    assert len(res) == 0

    res = scidb_con.iquery("show('xinput(\\'{}\\')', 'afl')".format(url),
                           fetch=True)
    assert res['schema'][0] == schema


def test_create_small(scidb_con):
    name = 'small_array'
    url = '{}/api/create_{}'.format(test_url, name)
    schema = '<v:int64> [i=0:19:0:10; j=0:19:0:10]'

    # Create
    array = scidbbridge.Array(url, schema)

    # Create First Chunk
    chunk = array.get_chunk(0, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (10, 11),
                                        'i': (0, 1),
                                        'j': (10, 10)}))
    chunk.save()

    # Create Second Chunk
    chunk = array.get_chunk(10, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (100, 100),
                                        'i': (10, 10),
                                        'j': (18, 19)}))
    chunk.save()

    # Create Empty Chunk
    chunk = array.get_chunk(0, 0)
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pandas.DataFrame())
    assert str(ex.value).startswith('Pandas DataFrame is empty')
    with pytest.raises(Exception) as ex:
        chunk.from_pandas(pandas.DataFrame({'v': (),
                                            'i': (),
                                            'j': ()}))
    assert str(ex.value).startswith('Pandas DataFrame is empty')

    # Create Index
    chunks = array.build_index()
    array.write_index(chunks)

    res = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    assert len(res) == 4
    res = res.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(
        res,
        pandas.DataFrame({'i': (0, 1, 10, 10),
                          'j': (10, 10, 18, 19),
                          'v': map(float, (10, 11, 100, 100))}))

    res = scidb_con.iquery("show('xinput(\\'{}\\')', 'afl')".format(url),
                           fetch=True)
    assert res['schema'][0] == schema


def test_create_unbound(scidb_con):
    name = 'unbound_array'
    url = '{}/api/create_{}'.format(test_url, name)
    schema = '<v:int64> [i=0:*:0:10; j=0:*:0:10]'

    # Create
    array = scidbbridge.Array(url, schema)

    # Create First Chunk
    chunk = array.get_chunk(0, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (10, 11),
                                        'i': (0, 1),
                                        'j': (10, 10)}))
    chunk.save()

    # Create Second Chunk
    chunk = array.get_chunk(10, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (100, 100),
                                        'i': (10, 10),
                                        'j': (18, 19)}))
    chunk.save()

    # Create Index
    chunks = array.build_index()
    array.write_index(chunks)

    res = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    assert len(res) == 4
    res = res.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(
        res,
        pandas.DataFrame({'i': (0, 1, 10, 10),
                          'j': (10, 10, 18, 19),
                          'v': map(float, (10, 11, 100, 100))}))

    res = scidb_con.iquery("show('xinput(\\'{}\\')', 'afl')".format(url),
                           fetch=True)
    assert res['schema'][0] == schema


@pytest.mark.parametrize('format,compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_create_format_compressed(scidb_con, format, compression):
    name = 'format_compressed'
    url = '{}/api/create_{}/{}/{}'.format(test_url, name, format, compression)
    schema = '<v:int64> [i=0:19:0:10; j=0:19:0:10]'

    # Create
    array = scidbbridge.Array(url=url,
                              schema=schema,
                              format=format,
                              compression=compression)

    # Create First Chunk
    chunk = array.get_chunk(0, 10)
    chunk.from_pandas(pandas.DataFrame({'v': (10, 11),
                                        'i': (0, 1),
                                        'j': (10, 10)}))
    chunk.save()

    # Create Index
    chunks = array.build_index()
    array.write_index(chunks)

    res = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    assert len(res) == 2
    res = res.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(
        res,
        pandas.DataFrame({'i': (0, 1),
                          'j': (10, 10),
                          'v': map(float, (10, 11))}))

    res = scidb_con.iquery("show('xinput(\\'{}\\')', 'afl')".format(url),
                           fetch=True)
    assert res['schema'][0] == schema

    # Get
    array2 = scidbbridge.Array(url=url)
    assert array2.metadata['compression'] == (None if compression == 'none'
                                              else compression)


def test_delta_attr(scidb_con):
    url = '{}/api/delta_attr'.format(test_url)
    schema = '<delta:int64> [i=0:19:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data={'i': range(0, 20, 5)}))

    for i in range(0, 20, 5):
        array.get_chunk(i).to_pandas()


def test_delta_dim(scidb_con):
    url = '{}/api/delta_dim'.format(test_url)
    schema = '<v:int64> [delta=0:19:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, delta),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data={'delta': range(0, 20, 5)}))

    for i in range(0, 20, 5):
        array.get_chunk(i).to_pandas()


@pytest.mark.parametrize('format, compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_filter(scidb_con, format, compression):
    url = '{}/api/filter/{}/{}'.format(test_url, format, compression)
    schema = '<v:int64, w:double> [i=0:9:0:5; j=10:19:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  filter(
    apply(
      build({}, j + i),
      w, double(v * v)),
    i >= 5 and w % 2 = 0),
  '{}',
  format:'{}',
  compression:'{}')""".format(schema.replace(', w:double', ''),
                              url,
                              format,
                              compression))

    array = scidbbridge.Array(url)
    chunks = array.read_index()

    pandas.testing.assert_frame_equal(
        chunks,
        pandas.DataFrame(data={'i': 5, 'j': (10, 15)}))

    for j_st in (10, 15):
        cells = []
        for i in range(5, 10):
            for j in range(j_st, j_st + 5):
                v = i + j
                w = float(v * v)
                if w % 2 == 0:
                    cells.append([v, w, i, j])

        pandas.testing.assert_frame_equal(
            array.get_chunk(5, j_st).to_pandas(),
            pandas.DataFrame(dict(zip('vwij', zip(*cells)))))


def test_delete_small(scidb_con):
    name = 'small_array'
    url = '{}/api/delete_{}'.format(test_url, name)
    schema = '<v:int64> [i=0:19:0:10; j=0:19:0:10]'

    for i in range(2):
        # Create
        array = scidbbridge.Array(url, schema)

        # Create First Chunk
        chunk = array.get_chunk(0, 10)
        chunk.from_pandas(pandas.DataFrame({'v': (10, 11),
                                            'i': (0, 1),
                                            'j': (10, 10)}))
        chunk.save()

        # Create Second Chunk
        chunk = array.get_chunk(10, 10)
        chunk.from_pandas(pandas.DataFrame({'v': (100, 100),
                                            'i': (10, 10),
                                            'j': (18, 19)}))
        chunk.save()

        # Create Index
        chunks = array.build_index()
        array.write_index(chunks)

        res = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
        assert len(res) == 4
        res = res.sort_values(by=['i', 'j']).reset_index(drop=True)
        pandas.testing.assert_frame_equal(
            res,
            pandas.DataFrame({'i': (0, 1, 10, 10),
                              'j': (10, 10, 18, 19),
                              'v': map(float, (10, 11, 100, 100))}))

        res = scidb_con.iquery("show('xinput(\\'{}\\')', 'afl')".format(url),
                               fetch=True)
        assert res['schema'][0] == schema

        # Delete array
        array.delete()
