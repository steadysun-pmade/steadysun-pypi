.. Steadysun documentation master file, created by
   sphinx-quickstart on Mon Oct  7 00:24:33 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Steadysun python documentation
==============================

This is a Python package designed to facilitate interaction with the **Steadysun** API.

This package provides tools and utilities for interacting with our API,
which facilitates operations such as retrieving forecasts and managing photovoltaic systems.



Installation
------------

The first step is installing `Steadysun` (`link to Pypi`_)
Steadysun is a python project, so it can be installed like any other python library.
Every Operating System should have Python pre-installed,
so you should just have to run:

.. tabs::
    .. tab:: from PyPI
        .. code:: console

            $ pip install steadysun

    .. tab:: from GitHub
        .. code:: console

            $ git clone https://github.com/Steadysun/steadysun.git
            $ cd steadysun
            $ pip install -e .


.. note:: Advanced users can install this in a virtualenv if they wish.


.. toctree::
   :maxdepth: 2
   :caption: Getting Started

   introduction

.. toctree::
   :maxdepth: 2
   :caption: Forecast

   forecast

.. toctree::
   :maxdepth: 2
   :caption: PVSystem

   pvsystem

.. _link to Pypi: https://test.pypi.org/project/steadysun/
