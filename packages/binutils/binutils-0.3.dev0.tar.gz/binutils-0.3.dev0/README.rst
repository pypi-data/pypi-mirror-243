========
binutils
========

Copyright (c) 2022 Jérémie DECOCK (www.jdhp.org)

* Web site: http://www.jdhp.org/software_en.html#binutils
* Online documentation: https://jdhp.gitlab.io/binutils
* Examples: https://jdhp.gitlab.io/binutils/gallery/

* Notebooks: https://gitlab.com/jdhp/binutils-notebooks
* Source code: https://gitlab.com/jdhp/binutils
* Issue tracker: https://gitlab.com/jdhp/binutils/issues
* Pytest code coverage: https://jdhp.gitlab.io/binutils/htmlcov/index.html
* binutils on PyPI: https://pypi.org/project/binutils
* binutils on Anaconda Cloud: https://anaconda.org/jdhp/binutils


Description
===========

Python Binary Tools

Note:

    This project is still in beta stage, so the API is not finalized yet.


Dependencies
============

C.f. requirements.txt

.. _install:

Installation
============

Gnu/Linux
---------

Posix (Linux, MacOSX, WSL, ...)
-------------------------------

From the binutils source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    source env/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Windows
-------

From the binutils source code::

    conda deactivate         # Only if you use Anaconda...
    python3 -m venv env
    env\Scripts\activate.bat
    python3 -m pip install --upgrade pip
    python3 -m pip install -r requirements.txt
    python3 setup.py develop


Documentation
=============

* Online documentation: https://jdhp.gitlab.io/binutils
* API documentation: https://jdhp.gitlab.io/binutils/api.html


Example usage
=============

* Examples: https://jdhp.gitlab.io/binutils/gallery/


Build and run the Python Docker image
=====================================

Build the docker image
----------------------

From the binutils source code::

    docker build -t binutils:latest .

Run unit tests from the docker container
----------------------------------------

From the binutils source code::

    docker run binutils pytest

Run an example from the docker container
----------------------------------------

From the binutils source code::

    docker run binutils python3 /app/examples/hello.py


Bug reports
===========

To search for bugs or report them, please use the binutils Bug Tracker at:

    https://gitlab.com/jdhp/binutils/issues


License
=======

This project is provided under the terms and conditions of the `MIT License`_.


.. _MIT License: http://opensource.org/licenses/MIT
.. _command prompt: https://en.wikipedia.org/wiki/Cmd.exe
