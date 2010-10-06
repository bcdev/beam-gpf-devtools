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
    configFilePath = 'template.config'
config = ConfigParser.ConfigParser()
config.read(configFilePath)

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

csvWriter = csv.writer(open(resultsPath + '/' + resultFileName, 'w'), delimiter='\t')

optionConfig = util.getSectionMerely(config, OPTIONS_SECTION)
permutedOptions = util.getPermutedOptions(optionConfig)




# write header line
headerline = ['id']
for item in optionConfig:
    headerline.append(item[0])
headerline.extend(['duration', 'status', 'command'])
csvWriter.writerow(headerline)


commandCfgs = util.getSectionMerely(config, COMMANDS_SECTION)
for cmdCfg in commandCfgs:
    id = cmdCfg[0]
    baseCommand = cmdCfg[1]
    for i in range(len(permutedOptions)):  
        try:
            optionMap = permutedOptions[i]
            optionString = ''
            for keyValue in optionMap.items():
                currOpt = keyValue[1].strip()
                if len(currOpt) != 0:
                    optionString = optionString + ' ' + keyValue[1]
                              
            command = baseCommand.replace("${OPTIONS}", optionString)
            t0 = datetime.datetime.utcnow()
            runid = id + "_" + str(i) + "(" + optionString + ")"
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
                pass
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
            output = [id]
            for item in optionConfig:
                output.append(optionMap[item[0]])
            output.extend([delta, status, command])
            csvWriter.writerow(output)
            print("Completed[" + runid+"] took: " + str(delta)) 
            if clearTargetProductsDir:
                util.removeDir(targetProductsPath)
                os.makedirs(targetProductsPath)

print('FINISHED')