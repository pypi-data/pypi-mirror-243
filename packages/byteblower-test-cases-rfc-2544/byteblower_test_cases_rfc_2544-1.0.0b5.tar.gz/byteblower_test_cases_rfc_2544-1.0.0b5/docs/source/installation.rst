**************************
Installation & Quick start
**************************

Installation
============

Requirements
------------

* `ByteBlower Test Framework`_: ByteBlower |registered| is a traffic
  generator/analyser system for TCP/IP networks.
* Highcharts-excentis_: Used for generating graphs
* jinja2_: To create HTML reports

.. _ByteBlower Test Framework: https://pypi.org/project/byteblower-test-framework/.
.. _Highcharts-excentis: https://pypi.org/project/highcharts-excentis/
.. |registered| unicode:: U+00AE .. registered sign
.. _jinja2: https://pypi.org/project/Jinja2/

Prepare runtime environment
---------------------------

Python
^^^^^^

The ByteBlower Test Framework currently supports Python versions >= 3.7.

We recommend managing the runtime environment in a Python virtual
environment. This guarantees proper separation of the system-wide
installed Python and pip packages.

Important: Working directory
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

All the following sections expect that you first moved to your working
directory where you want to run this project. You may also want to create
your configuration files under a sub-directory of your choice.

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         cd 'c:\path\to\working\directory'

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      .. code-block:: shell

         cd '/path/to/working/directory'

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

         .. _About Execution Policies: https://go.microsoft.com/fwlink/?LinkID=135170

      Make sure to specify the Python version you're using.
      For example, for Python 3.8:

      .. code-block:: shell

         py -3.8 -m venv --clear env
         & ".\env\Scripts\activate.ps1"
         python -m pip install -U pip build

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      **Note**: *Mind the leading* ``.`` *which means* **sourcing**
      ``./env/bin/activate``.

      .. code-block:: shell

         python3 -m venv --clear env
         . ./env/bin/activate
         pip install -U pip build

Install the ByteBlower RFC 2544 throughput Test Case
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

First make sure that you *activated* your virtual environment:

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         & ".\env\Scripts\activate.ps1"

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      .. code-block:: shell

         . ./env/bin/activate

Then install (or update) the RFC 2544 throughput test case
and its dependencies:

.. code-block:: shell

   pip install -U byteblower-test-cases-rfc-2544

Quick start
===========

Command-line interface
----------------------

After providing the appropriate test setup and frame configurations,
the test script can be run either as Python module or as a command-line script.

Show help
^^^^^^^^^

To get help for the command-line arguments:

#. As a Python module:

   .. code-block:: shell

      # To get help for the command-line arguments:
      python -m byteblower.test_cases.rfc_2544 --help

#. As a command-line script:

   .. code-block:: shell

      # To get help for the command-line arguments:
      byteblower-test-cases-rfc-2544-throughput --help

Run a test
^^^^^^^^^^

To run the ByteBlower RFC 2544 throughput test case, you should first provide
your test configuration, or use this `configuration file example
<json/rfc_2544.json>`_ (copy it to your working directory),
after you make sure to update the example configuration to your actual setup
configuration (ByteBlower server host name or IP, source and destination ports)

The reports will be stored under a subdirectory ``reports/``.

.. tabs::

   .. group-tab:: Windows

      On Windows systems using PowerShell:

      .. code-block:: shell

         # Create reports folder to store HTML/JSON files
         md reports
         # Run test
         byteblower-test-cases-rfc-2544-throughput --report-path reports

   .. group-tab:: Linux and macOS

      On Unix-based systems (Linux, WSL, macOS):

      .. code-block:: shell

         # Create reports folder to store HTML/JSON files
         mkdir reports
         # Run test
         byteblower-test-cases-rfc-2544-throughput --report-path  reports

Integrated
^^^^^^^^^^

.. code-block:: python

   from byteblower.test_cases.rfc_2544 import run

   # Defining test configuration, report path and report file name prefix:
   test_config = {} # Here you should provide your test setup + frame(s') configuration(s)
   report_path = 'my-output-folder' # Optional: provide the path to the output folder, defaults to the current working directory
   report_prefix = 'my-dut-feature-test' # Optional: provide prefix of the output files, defaults to 'report'

   # Run the RFC 2544 throughput test:
   run(test_config, report_path=report_path, report_prefix=report_prefix)
