# BEGIN_COPYRIGHT
#
# Copyright (C) 2022-2023 Paradigm4 Inc.
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

import pytest

from conftest import *


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_one_dim(scidb_con, chunk_size):
    url = '{}/xremove/one_dim_{}'.format(test_url, chunk_size)
    schema = '<v:int64> [i=0:19:0:{}]'.format(chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Remove
    scidb_con.iquery("xremove('{}')".format(url))

    # Remove second time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}')".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_two_dim(scidb_con, chunk_size):
    url = '{}/xremove/one_dim_{}'.format(test_url, chunk_size)
    schema = '<v:int64> [i=0:19:0:{cs}; j=0:19:0:{cs}]'.format(
        cs=chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Remove
    scidb_con.iquery("xremove('{}')".format(url))

    # Remove 2nd time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}')".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_one_dim_force(scidb_con, chunk_size):
    url = '{}/xremove/one_dim_{}'.format(test_url, chunk_size)
    schema = '<v:int64> [i=0:19:0:{}]'.format(chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Remove
    scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Remove second time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


@pytest.mark.parametrize('chunk_size', (5, 10, 20))
def test_two_dim_force(scidb_con, chunk_size):
    url = '{}/xremove/one_dim_{}'.format(test_url, chunk_size)
    schema = '<v:int64> [i=0:19:0:{cs}; j=0:19:0:{cs}]'.format(
        cs=chunk_size)

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Remove
    scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Remove 2nd time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)


def test_missing_chunk(scidb_con):
    url = '{}/xremove/missing_chunk'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5; j=0:19:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i + j),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Delete one chunk
    scidbbridge.driver.Driver.delete(url + '/chunks/c_1_1')

    # Remove
    scidb_con.iquery("xremove('{}')".format(url))


@pytest.mark.skipif(not security_enable,
                    reason="Requires SciDB Enterprise Edition")
def test_non_admin(scidb_con):
    # Setup
    scidb_con.create_namespace(test_ns)
    scidb_con.create_user(test_user, test_password_hash)
    scidb_con.set_role_permissions(test_user, "'namespace'", test_ns, 'ru')

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    url = '{}/xremove/non_admin'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    # Store
    scidb_con2.iquery("""
xsave(
  build({}, i),
  '{}',
  namespace:{})""".format(schema, url, test_ns))

    # Input
    scidb_con2.iquery("xinput('{}')".format(url), fetch=True)

    # Remove as non-admin
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xremove('{}')".format(url))

    # Input
    scidb_con2.iquery("xinput('{}')".format(url), fetch=True)

    # Remove as admin
    scidb_con.iquery("xremove('{}')".format(url))

    # Remove as admin 2nd time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}')".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xinput('{}')".format(url), fetch=True)

    # ---
    # Cleanup
    scidb_con.drop_user(test_user)
    scidb_con.drop_namespace(test_ns)


@pytest.mark.skipif(not security_enable,
                    reason="Requires SciDB Enterprise Edition")
def test_no_metadata(scidb_con):
    # Setup
    scidb_con.create_user(test_user, test_password_hash)

    con_args = {'scidb_url': scidb_url,
                'scidb_auth': (test_user, test_password),
                'verify': False}
    scidb_con2 = scidbpy.connect(**con_args)

    url = '{}/xremove/no_metadata'.format(test_url)
    schema = '<v:int64> [i=0:19:0:5]'

    # Store
    scidb_con.iquery("""
xsave(
  build({}, i),
  '{}')""".format(schema, url))

    # Input
    scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # Delete metadata
    scidbbridge.driver.Driver.delete(url + '/metadata')

    # Remove by non-admin user
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con2.iquery("xremove('{}')".format(url))

    # Remove by admin user w/o force
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}')".format(url))

    # Remove by admin user w/ force
    scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Remove second time
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xremove('{}', force:true)".format(url))

    # Input
    with pytest.raises(requests.exceptions.HTTPError):
        scidb_con.iquery("xinput('{}')".format(url), fetch=True)

    # ---
    # Cleanup
    scidb_con.drop_user(test_user)


@pytest.mark.skipif(not test_url.startswith('file://'),
                    reason="Requires file:// URL")
def test_wrong_url(scidb_con):
    query = "xremove('{}')"

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
