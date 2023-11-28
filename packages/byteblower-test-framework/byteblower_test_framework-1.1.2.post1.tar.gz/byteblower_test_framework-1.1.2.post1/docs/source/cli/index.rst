**********************
Command-line interface
**********************

.. toctree::
   :maxdepth: 2
   :caption: Table of Contents
   :reversed:
   :hidden:

   config_file

Installation
============

Prepare runtime environment
---------------------------

We recommend managing the runtime environment in a Python virtual
environment. This guarantees proper separation of the system-wide
installed Python and pip packages.

Python virtual environment
^^^^^^^^^^^^^^^^^^^^^^^^^^

Make sure to use the right Python version (>= 3.7, <= 3.11),
list all Python versions installed in your machine by running:

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         py --list

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      *Use your distribution-specific tools to list
      the available Python versions.*

If no Python version is in the required range, you can download and install
Python 3.7 or above using your system package manager
or from https://www.python.org/ftp/python.

Prepare Python virtual environment: Create the virtual environment
and install/update ``pip`` and ``build``.

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

         **Note**: On Microsoft Windows, it may be required to enable the
         Activate.ps1 script by setting the execution policy for the user.
         You can do this by issuing the following PowerShell command:

         .. code-block:: shell

            PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

         See `About Execution Policies`_ for more information.

      Make sure to specify the Python version you're using.
      For example, for Python 3.8:

      .. code-block:: shell

         py -3.8 -m venv --clear env
         & ".\env\Scripts\activate.ps1"
         python -m pip install -U pip build

      .. _About Execution Policies: https://go.microsoft.com/fwlink/?LinkID=135170

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      **Note**:
      *Mind the leading* ``.`` *which means* **sourcing** ``./env/bin/activate``.

      .. code-block:: shell

         python3 -m venv --clear env
         . ./env/bin/activate
         pip install -U pip build

Install the ByteBlower Test Framework from PyPI
-----------------------------------------------

First make sure that your *activated* your virtual environment:

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         & ".\env\Scripts\activate.ps1"

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      .. code-block:: shell

         . ./env/bin/activate

Now install (or update) the ByteBlower Test Framework:

.. code-block:: shell

   pip install -U byteblower-test-framework

Using the command-line interface
================================

Prepare
-------

Make sure that your *activated* your Python virtual environment:

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         & ".\env\Scripts\activate.ps1"

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      .. code-block:: shell

         . ./env/bin/activate

Show help
---------

Let's give it a test run!

Use the following command to show the command line interface help:

For the Python module
^^^^^^^^^^^^^^^^^^^^^

Import the test framework and show the documentation for the
ByteBlower Test Framework command-line interface module.

.. code-block:: shell

   python

.. code-block:: python

   import byteblower_test_framework.cli
   help(byteblower_test_framework.cli)

For the command-line
^^^^^^^^^^^^^^^^^^^^

As shell command:

.. code-block:: shell

   byteblower-test-framework --help

As Python module:

.. code-block:: shell

   python -m byteblower_test_framework --help

Run test with default input/output files
----------------------------------------

The arguments of the command-line interface have the following defaults:

Configuration file
   ``byteblower_test_framework.json``

Configuration file search path
   ``.`` (*current directory*)

Report file path
   ``.`` (*current directory*)

This means that:

* The *configuration file* (``byteblower_test_framework.json``)
  will be loaded from the *current directory*
* The resulting reports will also be saved into the *current directory*.

As shell command
^^^^^^^^^^^^^^^^

.. code-block:: shell

   byteblower-test-framework

As Python module
^^^^^^^^^^^^^^^^

.. code-block:: shell

   python -m byteblower_test_framework

Run test with given input/output files
--------------------------------------

You can specify a different *config file* and *report path* using:

.. note::
   When the *config file* is an absolute path to the file, then
   the *config path* (``--config-path <config_path>``) is ignored.

As shell command
^^^^^^^^^^^^^^^^

.. code-block:: shell

   byteblower-test-framework --config-file path/to/my_test_config.json --report-path path/to/my_test_reports_directory

As Python module
^^^^^^^^^^^^^^^^

.. code-block:: shell

   python -m byteblower_test_framework --config-file path/to/my_test_config.json --report-path path/to/my_test_reports_directory

Test configuration
==================

In the current release, it is possible to supply a configuration file
in ``JSON`` format for running your tests.

Have a look at :doc:`config_file` for a complete overview
of the file format.
