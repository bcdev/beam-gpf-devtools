BEAM GPF Development Tools
==========================

This module provides a collection of development tools for developing, tuning and testing of processors developed
using the BEAM Graph Processing Framework (GPF). It currently comprises the following tools:

* `GraphGenTool`: Creates GraphML files derived from the directed acyclic graph (DAG) DAG given operator.
* `permgen.py`:   A Python tool that calls an executable by generating all permutations of a given of arguments.

GraphGenTool
------------

Usage:

    GraphGenMain <productPath> <graphmlPath> <operatorClass> [[<hideBands>] <hideProducts>]

permgen.py
----------

Call an executable in a configurable number of variants and generate a runtime report.

Usage:

    permgen.py [--config CONFIG] [--file FILE] [--timeout MINUTES] [--quite]

The `CONFIG` file comprises any number of `KEY = VALUE` pairs. There are three types of entries:

1. Define the possible values for a parameter: `cmd.param.PARAM_NAME = PARAM_LIST`
2. Define an environment variable: `cmd.env.ENV_NAME = ENV_VALUE`
3. Specify the command-line to be executed: `cmd.line = CMDLINE`

The values for `CMDLINE` and `ENV_VALUE` may contain references to
`PARAM_NAME` and `ENV_NAME` using the syntax `$NAME` or better `${NAME}`.

`PARAM_LIST` must evaluate to a Python 'iterable' comprising either scalar values or pairs of
the form `[VALUE, ALIAS]`. In the report written to `FILE`, `ALIAS` will then be used instead of `VALUE`.

Here is the contents of a sample `CONFIG` file:

    cmd.param.p1 = ['a', 'b', 'c']
    cmd.param.p2 = [[64, "small"], 128, [256, "mid"], 512, [1024, "big"], 2048, [4096, "biggest"]]
    cmd.param.p3 = ['-Dwidth=30', '-Dwidth=60', '-Dwidth=90']
    cmd.param.heap = [1024, 2048]
    cmd.param.source = [[File("batch.py"), "file1"], File("test.bat")]
    cmd.env.JVM_OPTIONS = -Xmx${heap}M
    cmd.line = test.bat $p1 $p2 $p3 -S${source}





