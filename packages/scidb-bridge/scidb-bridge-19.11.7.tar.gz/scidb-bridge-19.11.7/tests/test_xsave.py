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
import os.path
import pandas
import pyarrow
import pytest
import requests

from conftest import *


@pytest.mark.parametrize('format, compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_one_chunk(scidb_con, format, compression):
    url = '{}/xsave/one_chunk/{}/{}'.format(test_url, format, compression)
    schema = '<v:int64> [i=0:9]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}',
  format:'{}',
  compression:'{}')""".format(schema, url, format, compression))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {
        **base_metadata,
        **{'schema': '{}'.format(
            schema.replace(']', ':0:1000000]')),
           'format': format,
           'compression': None if compression == 'none' else compression}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data={'i': range(1)}))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0).to_pandas(),
        pandas.DataFrame(data={'v': range(10), 'i': range(10)}))


@pytest.mark.parametrize('format, compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_multi_chunk(scidb_con, format, compression):
    url = '{}/xsave/multi_chunk/{}/{}'.format(test_url, format, compression)
    schema = '<v:int64> [i=0:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}',
  format:'{}',
  compression:'{}')""".format(schema, url, format, compression))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {
        **base_metadata,
        **{'schema': '{}'.format(schema),
           'format': format,
           'compression': None if compression == 'none' else compression}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data={'i': range(0, 20, 5)}))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0).to_pandas(),
        pandas.DataFrame(data={'v': range(5), 'i': range(5)}))
    pandas.testing.assert_frame_equal(
        array.get_chunk(10).to_pandas(),
        pandas.DataFrame(data={'v': range(10, 15), 'i': range(10, 15)}))


@pytest.mark.parametrize('format, compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_multi_dim(scidb_con, format, compression):
    url = '{}/xsave/multi_dim/{}/{}'.format(test_url, format, compression)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}',
  format:'{}',
  compression:'{}')""".format(schema, url, format, compression))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {
        **base_metadata,
        **{'schema': '{}'.format(schema),
           'format': format,
           'compression': None if compression == 'none' else compression}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 9, 5)
                               for j in range(10, 20, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i, i, j)
                               for i in range(5)
                               for j in range(10, 15)),
                         columns=('v', 'i', 'j')))


@pytest.mark.parametrize('format, compression',
                         itertools.product(('arrow', 'parquet'),
                                           ('none', 'gzip', 'lz4')))
def test_multi_atts(scidb_con, format, compression):
    url = '{}/xsave/multi_attr/{}/{}'.format(test_url, format, compression)
    schema = '<v:int64,w:double> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  apply(
    build({}, i),
    w, double(v * v)),
  '{}',
  format:'{}',
  compression:'{}')""".format(schema.replace(',w:double', ''),
                              url,
                              format,
                              compression))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {
        **base_metadata,
        **{'schema': '{}'.format(schema),
           'format': format,
           'compression': None if compression == 'none' else compression}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 9, 5)
                               for j in range(10, 20, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i, float(i * i), i, j)
                               for i in range(5)
                               for j in range(10, 15)),
                         columns=('v', 'w', 'i', 'j')))


def test_filter(scidb_con):
    url = '{}/xsave/filter'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    (i < 3 or i > 5) and j > 15),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, 15) for i in range(0, 9, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 15).to_pandas(),
        pandas.DataFrame(data=((i, i, j)
                               for i in range(3)
                               for j in range(16, 20)),
                         columns=('v', 'i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(5, 15).to_pandas(),
        pandas.DataFrame(data=((i, i, j)
                               for i in range(6, 10)
                               for j in range(16, 20)),
                         columns=('v', 'i', 'j')))


def test_empty_chunks(scidb_con):
    url = '{}/xsave/empty_chunks'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5; j=10:49:0:10]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i + j),
    (i >= 5 and i < 10 or i >= 15) and (j < 20 or j >= 30 and j < 40)),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in (5, 15)
                               for j in (10, 30)),
                         columns=('i', 'j')))

    for i_st in (5, 15):
        for j_st in (10, 30):
            pandas.testing.assert_frame_equal(
                array.get_chunk(i_st, j_st).to_pandas(),
                pandas.DataFrame(data=((i + j, i, j)
                                       for i in range(i_st, i_st + 5)
                                       for j in range(j_st, j_st + 10)),
                                 columns=('v', 'i', 'j')))


def test_one_index(scidb_con):
    prefix = 'one_index'
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:99:0:5; j=0:99:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}')""".format(schema, url))

    array = scidbbridge.Array(url)

    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 100, 5)
                               for j in range(0, 100, 5)),
                         columns=('i', 'j')))

    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 's3':
        index_prefix = '{}/xsave/{}/index/'.format(parts.path[1:], prefix)
        result = s3_con.list_objects_v2(Bucket=parts.netloc,
                                        Prefix=index_prefix)
        keys = [split['Key'] for split in result['Contents']]
    elif parts.scheme == 'file':
        index_prefix = '{}/xsave/{}/index/'.format(parts.path, prefix)
        keys = []
        for fn in os.listdir(index_prefix):
            key = index_prefix + fn
            if os.path.isfile(key):
                keys.append(key)
        keys.sort()

    assert keys == ['{}{}'.format(index_prefix, 0)]


@pytest.mark.parametrize('index_split', (100, 200, 400, 800))
def test_multi_index(scidb_con, index_split):
    prefix = 'multi_index_{}'.format(index_split)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:99:0:5; j=0:99:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}',
  index_split:{})""".format(schema, url, index_split))

    array = scidbbridge.Array(url)

    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 100, 5)
                               for j in range(0, 100, 5)),
                         columns=('i', 'j')))

    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 's3':
        index_prefix = '{}/xsave/{}/index/'.format(parts.path[1:], prefix)
        result = s3_con.list_objects_v2(Bucket=parts.netloc,
                                        Prefix=index_prefix)
        keys = [split['Key'] for split in result['Contents']]
    elif parts.scheme == 'file':
        index_prefix = '{}/xsave/{}/index/'.format(parts.path, prefix)
        keys = []
        for fn in os.listdir(index_prefix):
            key = index_prefix + fn
            if os.path.isfile(key):
                keys.append(key)
        keys.sort()

    assert keys == ['{}{}'.format(index_prefix, i)
                    for i in range(800 // index_split)]


@pytest.mark.parametrize('format', ('default', 'arrow', 'parquet'))
def test_format(scidb_con, format):
    prefix = 'format_{}'.format(format)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:19:0:5; j=10:49:0:10]'

    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}'{})""".format(schema,
                    url,
                    '' if format == 'default'
                    else ", format:'{}'".format(format)))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema),
                                 'format': '{}'.format(
                                     'arrow' if format == 'default'
                                     else format)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 20, 5)
                               for j in range(10, 50, 10)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i + j, i, j)
                               for i in range(0, 5)
                               for j in range(10, 20)),
                         columns=('v', 'i', 'j')))


@pytest.mark.parametrize('compression, sz_min, sz_max',
                         zip(('default', 'none', 'gzip', 'lz4'),
                             (0, 1000, 0, 0),
                             (500, 9999, 500, 500)))
def test_compression(scidb_con, compression, sz_min, sz_max):
    prefix = 'compression_{}'.format(compression)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:19:0:5; j=10:49:0:10]'

    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}'{})""".format(schema,
                    url,
                    '' if compression == 'default'
                    else ", compression:'{}'".format(compression)))

    array = scidbbridge.Array(url)

    m_compression = (None if compression == 'none'
                     else 'lz4' if compression == 'default'
                     else compression)
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema),
                                 'compression': m_compression}}
    for i_st in (5, 15):
        for j_st in (10, 30):
            pandas.testing.assert_frame_equal(
                array.get_chunk(i_st, j_st).to_pandas(),
                pandas.DataFrame(data=((i + j, i, j)
                                       for i in range(i_st, i_st + 5)
                                       for j in range(j_st, j_st + 10)),
                                 columns=('v', 'i', 'j')))

    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 's3':
        sz = s3_con.head_object(Bucket=parts.netloc,
                                Key='{}/xsave/{}/chunks/c_0_0'.format(
                                    parts.path[1:], prefix))['ContentLength']
    elif parts.scheme == 'file':
        sz = os.path.getsize('{}/xsave/{}/chunks/c_0_0'.format(parts.path,
                                                               prefix))

    assert sz > sz_min
    assert sz < sz_max


@pytest.mark.parametrize('format, compression',
                         itertools.product(('default', 'arrow', 'parquet'),
                                           ('default', 'none', 'gzip', 'lz4')))
def test_format_compression(scidb_con, format, compression):
    prefix = 'format_compression/{}/{}'.format(format, compression)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:int64> [i=0:19:0:5; j=10:49:0:10]'

    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}'{}{})""".format(schema,
                      url,
                      '' if format == 'default'
                      else ", format:'{}'".format(format),
                      '' if compression == 'default'
                      else ", compression:'{}'".format(compression)))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    m_compression = (None if compression == 'none'
                     else 'lz4' if compression == 'default'
                     else compression)
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema),
                                 'format': '{}'.format(
                                     'arrow' if format == 'default'
                                     else format),
                                 'compression': m_compression}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 20, 5)
                               for j in range(10, 50, 10)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i + j, i, j)
                               for i in range(0, 5)
                               for j in range(10, 20)),
                         columns=('v', 'i', 'j')))


@pytest.mark.parametrize('url', (None,
                                 '',
                                 'foo',
                                 'foo://',
                                 'foo://bar/taz',
                                 's3',
                                 's3:',
                                 's3:/',
                                 's3://',
                                 's3:\\',
                                 's3:\\\\',
                                 'file',
                                 'file:',
                                 'file:/',
                                 'file://',
                                 'file:\\',
                                 ))
def test_bad_url(scidb_con, url):
    schema = '<v:int64> [i=0:9]'

    que = 'xsave(build({}, i){})'.format(
        schema, '' if url is None else ", '{}'".format(url))

    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(que)


def test_update_error(scidb_con):
    name = 'update_error_{}'.format(test_id)
    url = '{}/xsave/update_error'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # No "update:true"
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # "update:false"
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build({}, i),
  '{}', update:false)""".format(schema, url))

    # "update:'foo'"
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build({}, i),
  '{}', update:'foo')""".format(schema, url))

    # Mismatched lower dimension
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=-1:9:0:5; j=10:19:0:5], i),
  '{}', update:true)""".format(url))

    # Mismatched higher dimension
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true)""".format(url))

    # Mismatched chunk size
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:10; j=10:20:0:5], i),
  '{}', update:true)""".format(url))

    # Mismatched chunk overlap
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:5:5], i),
  '{}', update:true)""".format(url))

    # Set format
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, format:'arrow')""".format(url))

    # Set format
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, format:'parquet')""".format(url))

    # Set compression
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, compression:'gzip')""".format(url))

    # Set compression
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, compression:'lz4')""".format(url))

    # Set index_split
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, index_split:10000)""".format(url))

    # Set namespace
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build(<v:int64> [i=0:9:0:5; j=10:20:0:5], i),
  '{}', update:true, namespace:public)""".format(url))

    # Existing array w/ different attribute type
    scidb_con.iquery("""
store(
  build(<v:double> [i=0:9:0:5; j=10:19:0:5], i),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)

    # Existing array w/ different attribute name
    scidb_con.iquery("""
store(
  build(<w:int64> [i=0:9:0:5; j=10:19:0:5], i),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)

    # Existing array w/ different number of attributes
    scidb_con.iquery("""
store(
  apply(
    build(<v:int64> [i=0:9:0:5; j=10:19:0:5], i),
    w, double(j)),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)

    # Existing array w/ different number of dimensions
    scidb_con.iquery("""
store(
  build(<v:int64> [i=0:9:0:5], i),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)

    # Existing array w/ different dimension bounds
    scidb_con.iquery("""
store(
  build(<v:int64> [i=0:19:0:5; j=10:19:0:5], i),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)

    # Existing array w/ different dimension chunk size
    scidb_con.iquery("""
store(
  build(<v:int64> [i=0:9:0:5; j=10:19:0:10], i),
  {})""".format(name))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))
    scidb_con.remove(name)


def test_update_array(scidb_con):
    name = 'update_array_{}'.format(test_id)
    url = '{}/xsave/update_array'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    scidb_con.iquery("""
store(
  build({}, i + 1),
  {})""".format(schema, name))

    scidb_con.iquery("xsave({}, '{}', update:true)".format(name, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 9, 5)
                               for j in range(10, 20, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i + 1, i, j)
                               for i in range(5)
                               for j in range(10, 15)),
                         columns=('v', 'i', 'j')))

    # Cleanup
    scidb_con.remove(name)


def test_update_all(scidb_con):
    url = '{}/xsave/update_all'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    scidb_con.iquery("""
xsave(
  build({}, i + 1),
  '{}', update:true)""".format(schema, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 9, 5)
                               for j in range(10, 20, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i + 1, i, j)
                               for i in range(5)
                               for j in range(10, 15)),
                         columns=('v', 'i', 'j')))


def test_update_filter(scidb_con):
    url = '{}/xsave/update_filter'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    (i < 5 or j >= 15)and i % 3 = 0),
  '{}')""".format(schema, url))

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    i % 2 = 0),
  '{}', update:true)""".format(schema, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(0, 9, 5)
                               for j in range(10, 20, 5)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 10).to_pandas(),
        pandas.DataFrame(data=((i, i, j)
                               for i in range(5)
                               for j in range(10, 15)
                               if ((i < 5 or j >= 15) and i % 3 == 0 or
                                   i % 2 == 0)),
                         columns=('v', 'i', 'j')))


def test_update_filter_index(scidb_con):
    url = '{}/xsave/update_filter_index'.format(test_url)
    schema = '<v:int64> [i=0:2:0:1; j=0:2:0:1]'

    scidb_con.iquery("""
xsave(
  filter(
    build({}, i),
    i > 1),
  '{}')""".format(schema, url))

    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}', update:true)""".format(schema, url))

    array = scidbbridge.Array(url)

    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}
    pandas.testing.assert_frame_equal(
        array.read_index(),
        pandas.DataFrame(data=((i, j)
                               for i in range(3)
                               for j in range(3)),
                         columns=('i', 'j')))
    pandas.testing.assert_frame_equal(
        array.get_chunk(0, 0).to_pandas(),
        pandas.DataFrame(data=((i, i, j)
                               for i in range(1)
                               for j in range(1)),
                         columns=('v', 'i', 'j')))


@pytest.mark.parametrize('ty, value',
                         itertools.chain(
                             (('{}int{}'.format(u, s), 'i')
                              for u in ('', 'u')
                              for s in (8, 16, 32, 64)),

                             (('bool', 'i % 2'),
                              ('float', 'i + .1'),
                              ('double', 'i + .01'),
                              ('char', 'char(i)'),
                              ('string', "'foo' + string(i)"),
                              ('datetime', 'datetime(i)'))))
def test_types(scidb_con, ty, value):
    prefix = 'types_{}'.format(ty)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:{}> [i=0:19:0:5; j=10:19:0:5]'.format(ty)

    scidb_con.iquery("""
xsave(
  build({}, iif(i % 3 = 0, null, {})),
  '{}')""".format(schema,
                  value,
                  url))

    array = scidbbridge.Array(url)
    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}


@pytest.mark.parametrize('ty, value',
                         itertools.chain(
                             (('{}int{}'.format(u, s), 'i')
                              for u in ('', 'u')
                              for s in (8, 16, 32, 64)),

                             (('bool', 'i % 2'),
                              ('float', 'i + .1'),
                              ('double', 'i + .01'),
                              ('char', 'char(i)'),
                              ('string', "'foo' + string(i)"),
                              ('datetime', 'datetime(i)'))))
def test_update_types(scidb_con, ty, value):
    prefix = 'update_types_{}'.format(ty)
    url = '{}/xsave/{}'.format(test_url, prefix)
    schema = '<v:{}> [i=0:19:0:5; j=10:19:0:5]'.format(ty)

    scidb_con.iquery("""
xsave(
  filter(
    build({}, iif(i % 3 = 0, null, {})),
    i < 10 and i >= 10),
  '{}')""".format(schema,
                  value,
                  url))

    array = scidbbridge.Array(url)
    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}

    scidb_con.iquery("""
xsave(
  filter(
    build({}, iif(i % 2 = 0, null, {})),
    i >= 5 and i < 15),
  '{}', update:true)""".format(schema,
                               value,
                               url))

    array = scidbbridge.Array(url)
    assert array.__str__() == url
    assert array.metadata == {**base_metadata,
                              **{'schema': '{}'.format(schema)}}


@pytest.mark.skipif(not security_enable,
                    reason="Requires SciDB Enterprise Edition")
def test_permissions(scidb_con):
    # Setup
    scidb_con.create_namespace(test_ns)
    scidb_con.create_user(test_user, test_password_hash)

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    url = '{}/xsave/permissions'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    # FS Init
    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 'file':
        fs_path = os.path.join(parts.path, 'xsave')
        if not os.path.exists(fs_path):
            os.makedirs(fs_path)

    # Namespace missing
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("""
xsave(
  build({}, i),
  '{}_taz',
  namespace:taz)""".format(schema, url))

    # Public namespace
    scidb_con2.iquery("""
xsave(
  build({}, i),
  '{}_public')""".format(schema, url))
    scidb_con2.iquery("xinput('{}_public')".format(url))

    # w/o update permission
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("""
xsave(
  build({}, i),
  '{}_foo',
  namespace:{})""".format(schema, url, test_ns))

    # w/ update permission
    scidb_con.set_role_permissions(test_user, "'namespace'", test_ns, 'u')
    scidb_con2 = scidbpy.connect(**con_args)
    scidb_con2.iquery("""
xsave(
  build({}, i),
  '{}_foo',
  namespace:{})""".format(schema, url, test_ns))

    # w/o read permission
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xinput('{}_foo')".format(url))

    # w/ read permission
    scidb_con.set_role_permissions(test_user, "'namespace'", test_ns, 'ru')
    scidb_con2 = scidbpy.connect(**con_args)
    scidb_con2.iquery("xinput('{}_foo')".format(url))

    # Cleanup
    scidb_con.drop_user(test_user)
    scidb_con.drop_namespace(test_ns)


def test_missing_index(scidb_con):
    url = '{}/xsave/missing_index'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    query = """
xsave(
  filter(
    build({}, i * 10),
    i < 10),
  '{}', update:true)""".format(schema, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        {'i': range(20),
         'v': (float(i * 10) if i < 10 else float(i)
               for i in range(20))})
    pandas.testing.assert_frame_equal(array, array_gold)

    # Delete Index
    scidbbridge.driver.Driver.delete(url + '/index/0')

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)
    with pytest.raises(AssertionError):
        pandas.testing.assert_frame_equal(array, array_gold)
    pandas.testing.assert_frame_equal(
        array, pandas.DataFrame({'i': range(10),
                                 'v': (float(i * 10) for i in range(10))}))


def test_missing_index_big(scidb_con):
    url = '{}/xsave/missing_index_big'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1; j=0:9:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i * j),
  '{}', index_split:100)""".format(schema, url))

    query = """
xsave(
  filter(
    build({}, i * 10),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j, float(i * 10) if i < 10 and j < 5 else float(i * j))
              for i in range(20) for j in range(10)],
        columns=('i', 'j', 'v'))
    pandas.testing.assert_frame_equal(array, array_gold)

    # Delete From Index
    scidbbridge.driver.Driver.delete(url + '/index/0')

    # Update
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)


def test_missing_chunks(scidb_con):
    url = '{}/xsave/missing_chunks'.format(test_url)
    schema = '<v:int64> [i=0:19:0:1]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    query = """
xsave(
  filter(
    build({}, i * 10),
    i >= 10 and i < 15),
  '{}', update:true)""".format(schema, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        {'i': range(20),
         'v': (float(i) if i < 10 or i >= 15 else float(i * 10)
               for i in range(20))})
    pandas.testing.assert_frame_equal(array, array_gold)

    scidbbridge.driver.Driver.delete(url + '/chunks/c_10')

    # Update
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)


def test_wrong_index(scidb_con):
    url = '{}/xsave/wrong_index'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_build = schema.replace(', w:string', '')

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema_build, url))

    query = """
xsave(
  filter(
    apply(
      build({}, i * 10),
      w, string(v)),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema_build, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j) + ((float(i * 10), str(i * 10)) if i < 10 and j < 5
                        else (float(i * j), str(i * j)))
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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

    # Restore
    ar.write_index(index_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


def test_wrong_chunk(scidb_con):
    url = '{}/xsave/wrong_chunk'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_build = schema.replace(', w:string', '')

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema_build, url))

    query = """
xsave(
  filter(
    apply(
      build({}, i * 10),
      w, string(v)),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema_build, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j) + ((float(i * 10), str(i * 10)) if i < 10 and j < 5
                        else (float(i * j), str(i * j)))
              for i in range(20)
              for j in range(10)],
        columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    ar = scidbbridge.Array(url)
    ch = ar.get_chunk(0, 0)
    chunk_gold = ch.to_pandas()
    chunk_url = '{}/chunks/c_0_0'.format(url)

    # ---
    # Add Column to Chunk
    chunk = chunk_gold.copy(True)
    chunk['x'] = chunk['v']
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Chunk Compressed
    chunk = chunk_gold.copy(True)
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


def test_wrong_chunk_compressed(scidb_con):
    url = '{}/xsave/wrong_chunk_compressed'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_build = schema.replace(', w:string', '')

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}', compression:'gzip')""".format(schema_build, url))

    query = """
xsave(
  filter(
    apply(
      build({}, i * 10),
      w, string(v)),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema_build, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j) + ((float(i * 10), str(i * 10)) if i < 10 and j < 5
                        else (float(i * j), str(i * j)))
              for i in range(20)
              for j in range(10)],
        columns=('i', 'j', 'v', 'w'))
    pandas.testing.assert_frame_equal(array, array_gold)

    ar = scidbbridge.Array(url)
    ch = ar.get_chunk(0, 0)
    chunk_gold = ch.to_pandas()
    chunk_url = '{}/chunks/c_0_0'.format(url)

    # ---
    # Add Column to Chunk
    chunk = chunk_gold.copy(True)
    chunk['x'] = chunk['v']
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema, compression='gzip')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Chunk Not Compressed
    chunk = chunk_gold.copy(True)
    chunk_table = pyarrow.Table.from_pandas(chunk)
    scidbbridge.driver.Driver.write_table(
        chunk_table, chunk_url, chunk_table.schema)
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

    # Restore
    ch.from_pandas(chunk_gold)
    ch.save()
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)


def test_wrong_metadata(scidb_con):
    url = '{}/xsave/wrong_metadata'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_build = schema.replace(', w:string', '')

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema_build, url))

    query = """
xsave(
  filter(
    apply(
      build({}, i * 10),
      w, string(v)),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema_build, url)

    # Update
    scidb_con.iquery(query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j) + ((float(i * 10), str(i * 10)) if i < 10 and j < 5
                        else (float(i * j), str(i * j)))
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
            scidb_con.iquery(query)

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
    scidb_con.iquery(query)
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
                scidb_con.iquery(query)
        else:
            scidb_con.iquery(query)
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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

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
        scidb_con.iquery(query)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # ---
    # Write Text File as Metadata
    save_metadata(metadata_url, "foo")
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(query)

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

    url = '{}/xsave/wrong_namespace'.format(test_url)
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    schema_build = schema.replace(', w:string', '')

    # Store
    scidb_con.iquery("""
xsave(
  apply(
    build({}, i * j),
    w, string(v)),
  '{}')""".format(schema_build, url))

    query = """
xsave(
  filter(
    apply(
      build({}, i * 10),
      w, string(v)),
    i < 10 and j < 5),
  '{}', update:true)""".format(schema_build, url)

    # Update
    scidb_con2.iquery(query)

    # Input
    array = scidb_con2.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j) + ((float(i * 10), str(i * 10)) if i < 10 and j < 5
                        else (float(i * j), str(i * j)))
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
    metadata['namespace'] = test_ns
    save_metadata(metadata_url, metadata_dict2text(metadata))
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery(query)

    # Restore
    save_metadata(metadata_url, metadata_gold)
    array = scidb_con2.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)
    pandas.testing.assert_frame_equal(array, array_gold)

    # Cleanup
    scidb_con.drop_user(test_user)


@pytest.mark.skipif(not test_url.startswith('file://'),
                    reason="Requires file:// URL")
def test_wrong_url(scidb_con):
    schema = '<v:int64, w:string> [i=0:19:0:5; j=0:9:0:5]'
    query = """
xsave(
  apply(
    build(<v:int64> [i=0:19:0:5; j=0:9:0:5], i * j),
    w, string(v)),
  '{}')"""

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


def test_s3_server_side_encryption(scidb_con):
    url = '{}/xsave/s3_sse'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    if not url.startswith('s3://'):
        return

    # Wrong usage
    que = "xsave(build({}, i), '{}', {{}})".format(schema, url)
    for arg in ('s3_sse',
                's3_sse:0'
                's3_sse:true',
                "s3_sse:''",
                "s3_sse:'0'",
                "s3_sse:'true'",
                "s3_sse:'foo'"):
        with pytest.raises(requests.exceptions.HTTPError):
            scidb_con.iquery(que.format(arg))

    # Corect usage
    que = "xsave(build({}, i), '{}{{}}', {{}})".format(schema, url)
    i = 0
    for arg in ("s3_sse:'NOT_SET'",
                "s3_sse:'AES256'",
                "s3_sse:'aws:kms'"):
        scidb_con.iquery(que.format(i, arg))
        i += 1


def test_end_chunk(scidb_con):
    url = '{}/xsave/end_chunk'.format(test_url)
    schema = '<x:int64>[i=-3:17:0:5; j=7:23:0:4; k=-100:-77:0:7]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i * j * k),
  '{}')""".format(schema, url))

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j', 'k']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j, k, float(i * j * k))
              for i in range(-3, 17 + 1)
              for j in range(7, 23 + 1)
              for k in range(-100, -77 + 1)],
        columns=('i', 'j', 'k', 'x'))
    pandas.testing.assert_frame_equal(array, array_gold)


def test_chunk_overlap(scidb_con):
    url = '{}/xsave/chunk_overlap'.format(test_url)

    schema = '<x:int64>[i=0:9:4:5]'
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave(build({}, i), '{}')".format(schema, url))

    schema = '<x:int64>[i=0:9:0:5; j=-100:99:2:10]'
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave(build({}, i), '{}')".format(schema, url))

    schema = '<x:int64>[i=0:9:0:5; j=-100:99:1:10; k=0:9:0:5]'
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xsave(build({}, i), '{}')".format(schema, url))


def test_not_empty(scidb_con):
    url = '{}/xsave/not_empty'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5; j=0:9:0:5]'

    # Store
    xsave_query = """
xsave(
  build({}, i * j),
  '{}')""".format(schema, url)
    scidb_con.iquery(xsave_query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
    array = array.sort_values(by=['i', 'j']).reset_index(drop=True)

    array_gold = pandas.DataFrame(
        data=[(i, j, float(i * j))
              for i in range(20)
              for j in range(10)],
        columns=('i', 'j', 'v'))
    pandas.testing.assert_frame_equal(array, array_gold)

    # Delete Metadata
    scidbbridge.driver.Driver.delete(url + '/metadata')
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery(xsave_query.replace('i * j', 'i + j'))


@pytest.mark.skipif(not security_enable,
                    reason="Requires SciDB Enterprise Edition")
def test_create_path(scidb_con):
    # Setup
    scidb_con.create_user(test_user, test_password_hash)

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    path = 'xsave/path'
    url = f'{test_url}/{path}/foo/bar'.format(test_url)
    schema = '<v:int64> [i=0:9:0:5; j=10:19:0:5]'

    # Queries
    xsave_query = """
xsave(
  build({}, i * j),
  '{}')""".format(schema, url)
    xremove_query = f"xremove('{url}')"

    # # As regular user
    scidb_con2 = scidbpy.connect(**con_args)
    scidb_con2.iquery(xsave_query)
    scidb_con2.iquery(xremove_query)

    # FS Cleanup
    parts = urllib.parse.urlparse(test_url)
    if parts.scheme == 'file':
        fs_path = os.path.join(parts.path, 'xsave/path')
        try:
            shutil.rmtree(fs_path)
        except PermissionError:
            pass
        except FileNotFoundError:
            pass

    # As root
    scidb_con.iquery(xsave_query)
    scidb_con.iquery(xremove_query)

    # Cleanup
    scidb_con.drop_user(test_user)


def test_list_operators(scidb_con):
    url = '{}/xsave/list_operators'.format(test_url)

    # Store
    xsave_query = """
xsave(
  list('operators'),
  '{}')""".format(url)
    scidb_con.iquery(xsave_query)

    # Input
    array = scidb_con.iquery("xinput('{}')".format(url), fetch=True)
