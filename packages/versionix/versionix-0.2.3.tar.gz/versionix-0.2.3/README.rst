Versionix
###########


.. image:: https://badge.fury.io/py/versionix.svg
    :target: https://pypi.python.org/pypi/versionix


.. image:: https://github.com/sequana/versionix/actions/workflows/main.yml/badge.svg
   :target: https://github.com/sequana/versionix/actions/workflows/main.yml

.. image:: https://coveralls.io/repos/github/sequana/versionix/badge.svg?branch=main
    :target: https://coveralls.io/github/sequana/versionix?branch=main

.. image:: https://zenodo.org/badge/658721856.svg
   :target: https://zenodo.org/badge/latestdoi/658721856

:Python version: Python 3.8, 3.9, 3.10, 3.11
:Source: See  `http://github.com/sequana/versionix <https://github.com/sequana/versionix/>`__.
:Issues: Please fill a report on `github <https://github.com/sequana/versionix/issues>`__

Overview
========

Versionix is a simple tool that attemps to print on screen the version of a given standalone.

Installation
----------------

If you are in a hurry, just type::

    pip install versionix  --upgrade

This is pure Python so no need for fancy libraries.

Usage
-----

Then, just type e.g::

    versionix  fastqc

This tool uses a registry so it will work only with resgistered tools, which list can be obtained with::

    versionix --registered

Type::

    versionix --help 

to get more help like this example:

.. image:: doc/versionix_usage.png


DESCRIPTION
===========


The first difficulty is that standalone applications have different ways to obtain their version information. Some require the use of a long or short argument (--version or -v), while others do not require any argument at all. In addition, display channels (stdout or stderr) and formats of the version output differs between applications. To handle these various cases, we define a dictionnary of **metadata** related to the different standalones. These metadata helps in the identification of the command to run, the options to use, if the information is directed to stdout or stderr and the method to parse the output to obtain the version number.

Versionix is designed to be used with all Sequana pipelines and is not intended to be universal. It will only work for tools that are registered. You can add your own standalone version in the versionix/register.py file and provide a Pull Request.

Changelog
=========

========= ========================================================================
Version   Description
========= ========================================================================
0.2.3     More tools in the registry
0.2.2     add all tools required by sequana pipelines (oct 2023)
0.2.1     More tools added.
0.2       simplification. Add tests. Add more tools
0.1       first draft
========= ========================================================================
