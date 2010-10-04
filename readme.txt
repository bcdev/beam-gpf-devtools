GPF Testbed
~~~~~~~~~~~

The GPF Testbed logs the execution time of one or multiple GPF executions

The results are written into a file in the results directory.
The result file has the following naming convention:
Result_<YYYYMMDD-HHMMSS>.txt  

The configuration of the testbed is placed in the file testbed.config.
It follows id normal Python configuration file scheme.
[section]
<name>: <value>

The file has to sections:
[general]
Here are general properties stored, valid for multiple runs.
[graphs]
Here are the command line calls defined with the configuration for each call.
The path to gpt(.bat/.sh/.command) is omitted.
 