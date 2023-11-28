**************************************************************
ByteBlower Test Case: Traffic tests for low latency validation
**************************************************************

.. footer::
   Copyright |copy| |year| - Excentis N.V.

.. |copy| unicode:: U+00A9 .. copyright sign
.. |year| date:: %Y

Introduction
============

This package contains a test case to generate multiple types of traffic
patterns using the `ByteBlower Test Framework`_. The traffic patterns
are used to validate your network for low latency.

.. _ByteBlower Test Framework: https://pypi.org/project/byteblower-test-framework/.

Installation
============

Requirements
------------

* `ByteBlower Test Framework`_: ByteBlower |registered| is a traffic
  generator/analyser system for TCP/IP networks.

.. |registered| unicode:: U+00AE .. registered sign

Prepare runtime environment
---------------------------

We recommend managing the runtime environment in a Python virtual
environment. This guarantees proper separation of the system-wide
installed Python and pip packages.

Python
------

The ByteBlower Test Framework currently supports Python versions
3.7 up to 3.11.

Important: Working directory
----------------------------

All the following sections expect that you first moved to your working
directory where you want to run this project. You may also want to create
your configuration files under a sub-directory of your choice.

#. On Unix-based systems (Linux, WSL, macOS):

   .. code-block:: shell

      cd '/path/to/working/directory'

#. On Windows systems using PowerShell:

   .. code-block:: shell

      cd 'c:\path\to\working\directory'

Python virtual environment
--------------------------

Make sure to use the right Python version (>= 3.7, <= 3.11),
list all Python versions installed in your machine by running:

#. On Windows systems using PowerShell:

   .. code-block:: shell

      py --list

If no Python version is in the required range, you can download and install
Python 3.7 or above using your system package manager
or from https://www.python.org/ftp/python.

Prepare Python virtual environment: Create the virtual environment
and install/update ``pip`` and ``build``.

#. On Unix-based systems (Linux, WSL, macOS):

   **Note**: *Mind the leading* ``.`` *which means* **sourcing**
   ``./env/bin/activate``.

   .. code-block:: shell

      python3 -m venv --clear env
      . ./env/bin/activate
      pip install -U pip build

#. On Windows systems using PowerShell:

   **Note**: On Microsoft Windows, it may be required to enable the
   Activate.ps1 script by setting the execution policy for the user.
   You can do this by issuing the following PowerShell command:

   .. code-block:: shell

      PS C:> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

   See `About Execution Policies`_ for more information.

   Make sure to specify the python version you're using.
   For example, for Python 3.8:

   .. code-block:: shell

      py -3.8 -m venv --clear env
      & ".\env\Scripts\activate.ps1"
      python -m pip install -U pip build

   .. _About Execution Policies: https://go.microsoft.com/fwlink/?LinkID=135170

To install the ByteBlower low latency validation test case and
its dependencies, first make sure that you have activated your
virtual environment:

#. On Unix-based systems (Linux, WSL, macOS):

   .. code-block:: shell

      . ./env/bin/activate

#. On Windows systems using PowerShell:

   .. code-block:: shell

      ./env/Scripts/activate.ps1

Then, run:

.. code-block:: shell

   pip install -U byteblower-test-cases-low-latency

Quick start
===========

Command-line interface
----------------------

After providing the appropriate test setup and flow configurations, the
test script can be run either as python module or as a command-line script.

For example (*to get help for the command-line arguments*):

#. As a python module:

   .. code-block:: shell

      # To get help for the command-line arguments:
      python -m byteblower.test_case.low_latency --help

#. As a command-line script:

   .. code-block:: shell

      # To get help for the command-line arguments:
      byteblower-test-cases-low-latency --help

To run the ByteBlower low latency validation test case, you should first
provide your test configuration, or copy this `Configuration file example`_ to
``low_latency.json`` file you create in your working directory. Make sure to
update the example configuration to your actual setup configuration
(ByteBlower server host name or IP, source and destination ports)

The reports will be stored under a subdirectory ``reports/``.

#. On Unix-based systems (Linux, WSL, macOS):

   .. code-block:: shell

      # Optional: create low_latency.json, then copy the configuration to it
      touch low_latency.json
      # Create reports folder to store HTML/JSON files
      mkdir reports
      # Run test
      byteblower-test-case-low-latency --report-path reports

#. On Windows systems using PowerShell:

   .. code-block:: shell

      # Optional: create low_latency.json, then copy the configuration to it
      New-Item low_latency.json
      # Create reports folder to store HTML/JSON files
      md reports
      # Run test
      byteblower-test-case-low-latency --report-path reports

Integrated
----------

.. code-block:: python

   from byteblower.test_case.low_latency import run

   # Defining test configuration, report path and report file name prefix:
   test_config = {} # Here you should provide your test setup + frame(s') configuration(s)
   report_path = 'my-output-folder' # Optional: provide the path to the output folder, defaults to the current working directory
   report_prefix = 'my-dut-feature-test' # Optional: provide prefix of the output files, defaults to 'report'

   # Run the low latency validation test:
   run(test_config, report_path=report_path, report_prefix=report_prefix)

Configuration file example
--------------------------

.. code-block:: json

   {
       "server": "byteblower.example.com.",
       "ports": [
           {
               "name": "CMTS-NSI 1",
               "port_group": [
                   "nsi-lld"
               ],
               "interface": "trunk-1-3",
               "ipv4": "dhcp"
           },
           {
               "name": "CMTS-NSI 2",
               "port_group": [
                   "nsi-classic"
               ],
               "interface": "trunk-1-3",
               "ipv4": "dhcp"
           },
           {
               "name": "CMTS-NSI 3",
               "port_group": [
                   "nsi-classic"
               ],
               "interface": "trunk-1-3",
               "ipv4": "dhcp"
           },
           {
               "name": "CM-LAN 1",
               "port_group": [
                   "cpe-classic"
               ],
               "interface": "trunk-1-13",
               "ipv4": "dhcp",
               "nat": true
           },
           {
               "name": "CM-LAN 2",
               "port_group": [
                   "cpe-lld"
               ],
               "interface": "trunk-1-13",
               "ipv4": "dhcp",
               "nat": true
           },
           {
               "name": "CM-LAN 3",
               "port_group": [
                   "cpe-lld"
               ],
               "interface": "trunk-1-13",
               "ipv4": "dhcp",
               "nat": true
           }
       ],
       "flows": [
           {
               "name": "L4S_FB",
               "source": {
                   "port_group": [
                       "nsi-lld"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-lld"
                   ]
               },
               "type": "l4s_frame_blasting",
               "frame_size": 1514,
               "bitrate": 1.5e5,
               "dscp": "0x10",
               "l4s_ecn": "l4s",
               "analysis": {
                   "latency": true
               }
           },
           {
               "name": "FB_Flow",
               "source": {
                   "port_group": [
                       "nsi-lld"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-lld"
                   ]
               },
               "type": "frame_blasting",
               "frame_size": 60,
               "frame_rate": 850,
               "dscp": "0x2E",
               "add_reverse_direction": true,
               "analysis": {
                   "latency": true
               }
           },
           {
               "name": "HTTP_Flow",
               "source": {
                   "port_group": [
                       "nsi-classic"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-classic"
                   ]
               },
               "type": "http",
               "initial_time_to_wait": 2.0,
               "request_duration": 40.0,
               "receive_window_scaling": 12
           },
           {
               "name": "Conference_Flow",
               "type": "conference",
               "source": {
                   "port_group": [
                       "nsi-classic"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-classic"
                   ]
               },
               "video": {
                   "frame_size": 1024,
                   "udp_src": 3480,
                   "udp_dest": 50020,
                   "frame_rate": 2600,
                   "number_of_frames": 12000,
                   "analysis": {
                       "latency": true
                   }
               },
               "voice": {
                   "udp_src": 3479,
                   "udp_dest": 50000,
                   "frame_rate": 5000
               },
               "screenshare": {
                   "frame_size": 252,
                   "frame_rate": 580,
                   "initial_time_to_wait": 15.0,
                   "duration": 11.0
               }
           },
           {
               "name": "Gaming_Flow",
               "type": "gaming",
               "dscp": "0x2B",
               "source": {
                   "port_group": [
                       "nsi-classic"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-classic"
                   ]
               },
               "analysis": {
                   "max_threshold_latency": 10.0
               }
           },
           {
               "name": "Voice_Flow",
               "type": "voice",
               "dscp": "0x2B",
               "source": {
                   "port_group": [
                       "nsi-classic"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-classic"
                   ]
               },
               "udp_src": 3579,
               "udp_dest": 50022,
               "number_of_frames": 50020,
               "analysis": {
                   "mos": true
               }
           },
           {
               "name": "Dynamic_FB_Flow",
               "source": {
                   "port_group": [
                       "nsi-classic"
                   ]
               },
               "destination": {
                   "port_group": [
                       "cpe-classic"
                   ]
               },
               "type": "dynamic_frame_blasting",
               "frame_size": 124,
               "frame_rate": 1500,
               "analysis": {
                   "latency": true
               }
           }
       ],
       "report": {
           "html_report": true,
           "json_report": false,
           "junit_xml_report": false
       },
       "enable_scouting_flows": true,
       "maximum_run_time": 30.0
   }
