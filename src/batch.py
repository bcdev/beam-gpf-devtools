from string import Template
import csv
import os
import sys
import time
import subprocess
import perm
import datetime

class File():
    path = ""

    def __init__(self, path):
        self.path = path

    def __str__(self):
        return self.path

class Parameter():
    name = None
    values = None
    aliases = None
    has_supplemental_value = False
    supplemental_name = ""

    def __init__(self, name, values, aliases):
        self.name = name
        self.values = values
        self.aliases = aliases
        if isinstance(self.values[0], File) :
            self.has_supplemental_value = True
            self.supplemental_name = "size"

    def getSupplementalValue(self, index):
        value = self.values[index]
        if isinstance(value, File) :
            return os.path.getsize(value.path)
        else:
            return ""

    def hasAlias(self, index):
        return self.aliases[index] is not None

    def getAlias(self, index):
        return self.aliases[index]


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
        # because of the aliases we need two dictionaries;
        # one for substitution in the command line and one for the csv file
        cmd_param_dict = dict()
        csv_param_dict = dict()
        for i in range(len(indexes)):
            j = indexes[i]
            param = self._parameters[i]
            cmd_param_dict[param.name] = param.values[j]
            if param.has_supplemental_value :
                cmd_param_dict[param.supplemental_name] = param.getSupplementalValue(j)
                csv_param_dict[param.supplemental_name] = param.getSupplementalValue(j)
            if param.hasAlias(j):
                csv_param_dict[param.name] = param.getAlias(j)
            else:
                csv_param_dict[param.name] = param.values[j]

        env_dict = dict()
        for key in self._env_dict:
            env_dict[key] = Template(self._env_dict[key]).safe_substitute(cmd_param_dict)

        command = Template(self._command).safe_substitute(cmd_param_dict)
        if self._options.verbose :
            print(command)
        t0 = datetime.datetime.utcnow()
        process = subprocess.Popen(command, env=env_dict, shell=True)
        status = None
        try:
            while process.poll() is None :
                time.sleep(0.1)
                tempDelta = datetime.datetime.utcnow() - t0
                if self._options.timeout > 0 and tempDelta.total_seconds() > self._options.timeout * 60:
                    process.kill()
                    status='timeout'
        except SystemExit as se:
            process.kill()
            raise se
        if status is None:
            status = "Completed"
        delta = datetime.datetime.utcnow() - t0
        csv_param_dict['time'] = delta.total_seconds()
        csv_param_dict['status'] = status
        csv_param_dict['command'] = command
        self._writer.writerow(csv_param_dict)

    def get_values_and_aliases(self, evaluated_list) :
        values = []
        aliases = []
        for item in evaluated_list:
            if isinstance(item, list):
                values.append(item[0])
                aliases.append(item[1])
            else :
                values.append(item)
                aliases.append(None)
        return (values, aliases)

    def run(self):
        config_dict = dict()
        env_dict = dict()
        with open(self._options.config_file) as f:
            for line in f:
                line = line.strip()
                if line.startswith('#') or line == "":
                    continue
                # read further if line ends with line continuation character
                while line.endswith('\\') :
                    line = line.rstrip('\\')
                    temp_line = f.next().strip()
                    line = line + temp_line
                stripper = lambda s: s.strip()
                tokens = map(stripper, line.split('=', 1))
                name = tokens[0]
                config_values = Template(tokens[1]).safe_substitute(config_dict)
                if name.startswith(self.PREFIX_COMMAND_ENV):
                    env_dict[name[len(self.PREFIX_COMMAND_ENV):]] = config_values
                if name.startswith(self.PREFIX_COMMAND_PARAM):
                    eval_values = eval(config_values)
                    (values, aliases) = self.get_values_and_aliases(eval_values)
                    config_dict[name] = values
                    self._parameters.append(Parameter(name[len(self.PREFIX_COMMAND_PARAM):], values, aliases))
                else:
                    config_dict[name] = config_values


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
        column_names.extend(['time', 'status','command'])

        self._writer = csv.DictWriter(csvfile, column_names)
        self._writer.writeheader()
        parameter_values =[]
        for p in self._parameters :
            parameter_values.append(p.values)
        self.loop(self.get_dim_sizes(parameter_values))

        if self._options.output_file is not None:
            csvfile.close()
