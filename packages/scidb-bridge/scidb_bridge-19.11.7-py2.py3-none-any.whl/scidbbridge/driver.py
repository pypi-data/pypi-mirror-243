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
import os
import pyarrow
import pyarrow.parquet
import urllib.parse
import shutil


class Driver:
    default_format = 'arrow'
    default_compression = 'lz4'

    index_format = 'arrow'
    index_compression = 'lz4'

    _s3_client = None
    _s3_resource = None

    @staticmethod
    def s3_client():
        if Driver._s3_client is None:
            Driver._s3_client = boto3.client('s3')
        return Driver._s3_client

    @staticmethod
    def s3_resource():
        if Driver._s3_resource is None:
            Driver._s3_resource = boto3.resource('s3')
        return Driver._s3_resource

    @staticmethod
    def list(url):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:] + '/'
            pages = Driver.s3_client().get_paginator(
                'list_objects_v2').paginate(Bucket=bucket, Prefix=key)
            for page in pages:
                if 'Contents' in page.keys():
                    for obj in page['Contents']:
                        yield 's3://{}/{}'.format(bucket, obj['Key'])

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            for fn in os.listdir(path):
                if os.path.isfile(os.path.join(path, fn)):
                    yield 'file://' + os.path.join(path, fn)

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def init_array(url):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            pass

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            os.makedirs(path, exist_ok=True)
            os.mkdir(os.path.join(path, 'index'))
            os.mkdir(os.path.join(path, 'chunks'))

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def read_metadata(url):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:] + '/metadata'
            obj = Driver.s3_client().get_object(Bucket=bucket, Key=key)
            return obj['Body'].read().decode('utf-8')

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path, 'metadata')
            return open(path).read()

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def write_metadata(url, metadata):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:] + '/metadata'
            Driver.s3_client().put_object(Body=metadata,
                                          Bucket=bucket,
                                          Key=key)

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path, 'metadata')
            with open(path, 'w') as f:
                f.write(metadata)

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def read_table(url,
                   format=default_format,
                   compression=default_compression):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:]
            obj = Driver.s3_client().get_object(Bucket=bucket, Key=key)
            buf = pyarrow.py_buffer(obj['Body'].read())
            if format == 'arrow':
                strm = pyarrow.input_stream(buf,
                                            compression=compression)
                return pyarrow.RecordBatchStreamReader(strm).read_all()
            elif format == 'parquet':
                return pyarrow.parquet.read_table(buf)
            else:
                raise Exception('Format {} not supported'.format(format))

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            if format == 'arrow':
                strm = pyarrow.input_stream(path, compression=compression)
                return pyarrow.RecordBatchStreamReader(strm).read_all()
            if format == 'parquet':
                return pyarrow.parquet.read_table(path)
            else:
                raise Exception('Format {} not supported'.format(format))

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def write_table(table,
                    url,
                    schema,
                    format=default_format,
                    compression=default_compression):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:]
            buf = pyarrow.BufferOutputStream()
            if format == 'arrow':
                stream = pyarrow.output_stream(buf, compression=compression)
                writer = pyarrow.RecordBatchStreamWriter(stream, schema)
                writer.write_table(table)
                writer.close()
                stream.close()
            elif format == 'parquet':
                pyarrow.parquet.write_table(
                    table, buf, compression=compression)
            else:
                raise Exception('Format {} not supported'.format(format))
            Driver.s3_client().put_object(Body=buf.getvalue().to_pybytes(),
                                          Bucket=bucket,
                                          Key=key)

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            if format == 'arrow':
                stream = pyarrow.output_stream(path, compression=compression)
                writer = pyarrow.RecordBatchStreamWriter(stream, schema)
                writer.write_table(table)
                writer.close()
                stream.close()
            elif format == 'parquet':
                pyarrow.parquet.write_table(
                    table, path, compression=compression)
            else:
                raise Exception('Format {} not supported'.format(format))

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def delete_all(url):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:]
            Driver.s3_resource().Bucket(
                bucket).objects.filter(Prefix=key).delete()

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            for fn in os.listdir(path):
                tfn = os.path.join(path, fn)
                if os.path.isdir(tfn):
                    shutil.rmtree(tfn)
                else:
                    os.unlink(tfn)

        else:
            raise Exception('URL {} not supported'.format(url))

    @staticmethod
    def delete(url):
        parts = urllib.parse.urlparse(url)

        # S3
        if parts.scheme == 's3':
            bucket = parts.netloc
            key = parts.path[1:]
            Driver.s3_client().delete_object(Bucket=bucket, Key=key)

        # File System
        elif parts.scheme == 'file':
            path = os.path.join(parts.netloc, parts.path)
            os.unlink(path)

        else:
            raise Exception('URL {} not supported'.format(url))
