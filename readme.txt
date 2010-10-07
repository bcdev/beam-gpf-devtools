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
Insert in this section the command which shall be executed.
You can reference the options defined in the OPTIONS sections 
with the following syntax: ${optionName}.
[OPTIONS]
Define here the options which shall be iterated.
If a special value shall be put into the result table instead of the option value  
use the following syntax for an option:
<optionValue>#<outputValue>