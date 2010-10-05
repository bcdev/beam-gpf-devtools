GPF Testbed
~~~~~~~~~~~

The GPF Testbed logs the execution time of one or multiple GPF executions

The results are written into a file in the results directory.
The result file has the following naming convention:
Result_<YYYYMMDD-HHMMSS>.txt  

By default the configuration of the testbed is taken from the file testbed.config.
The configuration file can also be given as first command line parameter.
It follows the normal Python configuration file scheme.
[section]
<name>: <value>

The file has to sections:
[DEFAULT]
Here are general properties stored, valid for multiple runs.
[GRAPH]
Here are the command line calls defined with the configuration for each call.
The path to gpt(.bat/.sh/.command) is omitted.
 