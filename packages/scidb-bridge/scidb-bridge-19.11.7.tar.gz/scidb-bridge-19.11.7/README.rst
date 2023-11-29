SciDB-Bridge: Python Library to access externally stored SciDB data
===================================================================

.. image:: https://img.shields.io/badge/SciDB-23.10-blue.svg
    :target: https://paradigm4.atlassian.net/wiki/spaces/SD/pages/2967437320/23.10+Release+Notes

.. image:: https://img.shields.io/badge/arrow-11.0.0-blue.svg
    :target: https://arrow.apache.org/release/11.0.0.html


Requirements
------------

- Python ``3.5.x``, ``3.6.x``, ``3.7.x``, ``3.8.x``, ``3.9.x``, or ``3.10.x``
- SciDB ``19.11`` or newer
- SciDB-Py ``19.11.7`` or newer
- Apache PyArrow ``5.0.0`` up to ``11.0.0``
- Boto3 ``1.14.12`` for Amazon Simple Storage Service (S3) support


Installation
------------

Install latest release::

  pip install scidb-bridge

Install development version from GitHub::

  pip install git+http://github.com/paradigm4/bridge.git#subdirectory=py_pkg


Contributing
------------

Check code style before committing code

.. code:: bash

  pip install pycodestyle
  pycodestyle py_pkg

For Visual Studio Code see `Linting Python in Visual Studio Code <https://code.visualstudio.com/docs/python/linting>`_
