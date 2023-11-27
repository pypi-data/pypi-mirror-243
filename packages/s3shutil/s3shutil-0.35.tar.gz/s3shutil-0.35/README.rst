===================================================
The easiest way to manipulate multiple files in s3
===================================================
|Unittests| |License| |Downloads| |Language|

.. |Unittests| image:: https://github.com/andyil/s3shutil/actions/workflows/unitests.yml/badge.svg
    
.. |Downloads| image:: https://img.shields.io/pypi/dw/s3shutil
    
.. |License| image:: https://img.shields.io/github/license/andyil/s3shutil
    :target: https://github.com/andyil/s3shutil/blob/develop/LICENSE
    :alt: License

.. |Language| image:: https://img.shields.io/github/languages/top/andyil/s3shutil

s3shutil is the easiest to use and fastest way of manipulating directory files in s3,
probably at the expense of hiding API details you don't usually care.

Installation
---------------
We recommend installing from the official PyPI repository.

.. code-block:: sh

    $ pip install s3shutil
    




Design Principles
~~~~~~~~~~~~~~~~~
* Expose a simple and intuitive string based API. 
* Where possible, emulate the well known `shutil <https://docs.python.org/3/library/shutil.html>`_ standard module API.
* Use multithreading behind the scenes for performance.
* Internally use batch APIs where available (deleting objects).
* Internally use server to server APIs where possible (copy between s3 to s3).


Using s3shutil
~~~~~~~~~~~~~~
s3shutil uses `boto3 <https://github.com/boto/boto3>`_ internally and we assume you have your credentials set up properly.

Using s3shutil is super easy:

**Download a directory tree from s3**:

.. code-block:: python
    
    import s3shutil
    s3shutil.copytree('s3://bucket/remote/files/', '/home/myuser/my-directory/')

**Upload a directory tree to s3.**

Just replace the order of the arguments, as you probably expected.

.. code-block:: python

    import s3shutil
    s3shutil.copytree('/home/myuser/documents', 's3://bucket/my-files/documents/')

**Copy a directory tree from s3 to another location in s3.**

Supports same or different bucket.

s3shutil will notice and use server to server (s3 object copy) for you.

.. code-block:: python

    import s3shutil
    s3shutil.copytree('s3://other-bucket/source-files/whatever/', 's3://bucket/my-files/documents/')

**Delete multiple files from s3.**

s3shutil will notice and internally use batch delete.

.. code-block:: python

    import s3shutil
    s3shutil.rmtree('s3://bucket/my-files/documents/')
