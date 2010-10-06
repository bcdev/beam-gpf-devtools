GPF Testbed
~~~~~~~~~~~

The GPF Testbed logs the execution time of one or multiple GPF executions

The results are written into a file in the results directory.
The result file has the following naming convention:
Result_<YYYYMMDD-HHMMSS>.txt  

Start the testbed by calling testbed.py.
By default the configuration of the testbed is taken from the file template.config.
The configuration file can also be given as first command line parameter.
It follows the normal Python configuration file scheme.
[section]
<name>: <value>

The file has to sections:
[DEFAULT]
Here are general properties stored, valid for multiple runs.
[COMMANDS]
Insert in this section the commands which shall be executed.
The place where the options shall be inserted is defined by ${OPTIONS}.
[OPTIONS]
Define here the options which shall be iterated. 