import os
import sys
import datetime
import time
import subprocess
import util
import csv
import ConfigParser

DEFAULT_SECTION = 'DEFAULT'
OPTIONS_SECTION = 'OPTIONS'
COMMANDS_SECTION = 'COMMANDS'

# Get the configuration from the given file or from the default 'testbed.config'
if len(sys.argv) > 1:
    configFilePath = sys.argv[1]
else:
    configFilePath = 'testbed.config'
config = ConfigParser.ConfigParser()
config.read(configFilePath)

print(config.get(DEFAULT_SECTION, 'beam.standard.home'))

targetProductsPath = config.get(DEFAULT_SECTION, 'targetdir')
timeoutValue = config.getint(DEFAULT_SECTION, 'timeout')
timeout = datetime.timedelta(minutes=timeoutValue)
clearTargetProductsDir = config.getboolean(DEFAULT_SECTION, 'targetdir.clear')

if clearTargetProductsDir and os.path.exists(targetProductsPath):
    util.removeDir(targetProductsPath)

currentTime = datetime.datetime.utcnow()
resultFileName = 'Result_' + currentTime.strftime("%Y%m%d-%H%M%S") + '.txt'
resultsPath = 'results'
if not os.path.exists(resultsPath):
    os.makedirs(resultsPath)

csvWriter = csv.writer(open(resultsPath + '/' + resultFileName, 'wb'), delimiter='\t')

optionConfig = util.getSectionMerely(config, OPTIONS_SECTION)
permutedOptions = util.getPermutedOptions(optionConfig)




# write header line
headerline = ['id']
for item in optionConfig:
    headerline.append(item[0])
headerline.extend(['duration', 'status', 'command'])
csvWriter.writerow(headerline)


commandCfgs = util.getSectionMerely(config, COMMANDS_SECTION)
print(commandCfgs)
for cmdCfg in commandCfgs:
    for i in range(len(permutedOptions)):
        try:
            id = cmdCfg[0]
            command = cmdCfg[1]
            optionMap = permutedOptions[i]
            optionString = ''
            for keyValue in optionMap.items():
                currOpt = keyValue[1][0]
                if len(currOpt) != 0:
                    command = command.replace('${'+keyValue[0]+'}', currOpt)
                else:
                    command = command.replace('${'+keyValue[0]+'}', currOpt)
            print(command)
            t0 = datetime.datetime.utcnow()
            runid = id + "_" + str(i)
            print("Starting [" + runid + "] at " + str(t0.time()))
            status = ''
            try:
                # TODO: Killing subprocess if started from IDE (Eclipse) does not work?
                process = subprocess.Popen(command)
                while process.poll() == None :
                    time.sleep(0.1)
                    tempDelta = datetime.datetime.utcnow() - t0
                    if timeoutValue > 0 and tempDelta > timeout:
                        process.kill()
                        status = 'Timeout'
            except SystemExit:
                process.terminate()
                status = 'Canceled'
            t1 = datetime.datetime.utcnow()
            delta = t1 - t0
        except Exception as e:
            print(e)
            status = 'ERROR'
        finally:
            if len(status) == 0:
                status = 'Completed'
            output = [runid]
            for item in optionConfig:
                output.append(optionMap[item[0]][1])
            output.extend([delta.total_seconds(), status, command])
            csvWriter.writerow(output)
            print("Completed[" + runid+"] took: " + str(delta))
            if clearTargetProductsDir:
                util.removeDir(targetProductsPath)
                os.makedirs(targetProductsPath)

print('FINISHED')
