from string import Template
import csv
import os
import sys
import time
import subprocess
import perm

class File():
    path = ""

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

class Parameter():
    name = None
    values = None
    has_supplemental_value = False
    supplemental_name = ""

    def __init__(self, name, values):
        self.name = name
        self.values = values
        if isinstance(self.values[0], File) :
            self.has_supplemental_value = True
            self.supplemental_name = "size"

    def getSupplementalValue(self, index):
        return os.path.getsize(self.values[index].path)



class Executer(perm.NestedFor):
    PREFIX_COMMAND_PARAM = "cmd.param."
    PREFIX_COMMAND_ENV = "cmd.env."
    NAME_COMMAND_LINE = "cmd.line"

    _param_names = []
    _parameters = []
    _env_dict = {}
    _command = ""
    _writer = None
    _options = None

    def __init__(self, options):
        self._options = options

    def do_element(self, indexes):
        param_dict = dict()
        for i in range(len(indexes)):
            j = indexes[i]
            param = self._parameters[i]
            param_dict[param.name] = param.values[j]
            if param.has_supplemental_value :
                param_dict[param.supplemental_name] = param.getSupplementalValue(j)

        env_dict = dict()
        for key in self._env_dict:
            env_dict[key] = Template(self._env_dict[key]).safe_substitute(param_dict)

        command = Template(self._command).safe_substitute(param_dict)

        t0 = time.clock()
        process = subprocess.Popen(command, env=env_dict)
        while process.poll() is None :
            try:
                time.sleep(0.1)
                tempDelta = time.clock() - t0
                if self._options.timeout > 0 and tempDelta > self._options.timeout:
                    process.kill()
            except SystemExit as se:
                process.terminate()
                raise se

        t1 = time.clock()
        param_dict['time'] = t1 - t0
        self._writer.writerow(param_dict)

    def run(self):
        config_dict = dict()
        env_dict = dict()
        with open(self._options.config_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == "":
                    continue
                stripper = lambda s: s.strip()
                tokens = map(stripper, line.split('=', 1))
                name = tokens[0]
                value = Template(tokens[1]).safe_substitute(config_dict)
                config_dict[name] = value
                if name.startswith(self.PREFIX_COMMAND_PARAM):
                    self._parameters.append(Parameter(name[len(self.PREFIX_COMMAND_PARAM):], eval(value)))
                if name.startswith(self.PREFIX_COMMAND_ENV):
                    env_dict[name[len(self.PREFIX_COMMAND_ENV):]] = value

        self._command = config_dict[self.NAME_COMMAND_LINE]
        self._env_dict = env_dict

        csvfile = sys.stdout
        if self._options.output_file is not None:
            csvfile = open(self._options.output_file, "wb")

        column_names = []
        for param in self._parameters:
            column_names.append(param.name)
            if param.has_supplemental_value :
                column_names.append(param.supplemental_name)
        column_names.append('time')

        self._writer = csv.DictWriter(csvfile, column_names)
        self._writer.writeheader()
        parameter_values =[]
        for p in self._parameters :
            parameter_values.append(p.values)
        self.loop(self.get_dim_sizes(parameter_values))

        if self._options.output_file is not None:
            csvfile.close()
