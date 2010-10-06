import os
import sys
import datetime
import time 
import subprocess
import util
import csv
import ConfigParser

DEFAULT_SECTION = 'DEFAULT'
COMMAND_SECTION = 'COMMAND'

# Get the configuration from the given file or from the default 'testbed.config'
if len(sys.argv) > 1:
    configFilePath = sys.argv[1]
else:
    configFilePath = 'testbed.config'
config = ConfigParser.ConfigParser()
config.read(configFilePath)

targetProductsPath = config.get(DEFAULT_SECTION, 'targetproductdir')
timeoutValue = config.getint(DEFAULT_SECTION, 'timeout')         
clearTargetProductsDir = config.getboolean(DEFAULT_SECTION, 'targetproductdir.clear')

if clearTargetProductsDir and os.path.exists(targetProductsPath):
    util.removeDir(targetProductsPath)    

currentTime = datetime.datetime.utcnow()
resultFileName = 'Result_' + currentTime.strftime("%Y%m%d-%H%M%S") + '.txt'    
resultsPath = 'results'
if not os.path.exists(resultsPath):
    os.makedirs(resultsPath)

csvWriter = csv.writer(open(resultsPath + '/' + resultFileName, 'w'), delimiter='\t')

graphConfigs = util.getSectionMerely(config, COMMAND_SECTION)

for graphItem in graphConfigs:  
    try:
        runId = graphItem[0]
        gptCommand = graphItem[1]

        t0 = datetime.datetime.utcnow()
        print("Starting [" + runId + "] at " + str(t0.time()))
        status = 'Completed'
        try:
            # TODO: Killing subprocess if started from IDE (Eclipse) does not work?
            process = subprocess.Popen(gptCommand)
            while process.poll() == None :
                time.sleep(0.1)
                tempDelta = datetime.datetime.utcnow() - t0
                if timeoutValue > 0 and tempDelta > datetime.timedelta(minutes=timeoutValue) :
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
        output = [runId, delta, status, gptCommand]
        csvWriter.writerow(output)
        print("[" + runId + ":" + status + "] took: " + str(delta)) 
        if clearTargetProductsDir:
            util.removeDir(targetProductsPath)
            os.makedirs(targetProductsPath)

print('FINISHED')
