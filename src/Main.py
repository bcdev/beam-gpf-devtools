import os
import sys
import datetime
import subprocess
import util
import csv
import ConfigParser 

# Get the configuration from the given file or from the default 'testbed.config'
if len(sys.argv) > 1:
    configFilePath = sys.argv[1]
else:
    configFilePath = 'testbed.config'
config = ConfigParser.ConfigParser()
config.read(configFilePath)

# setup path to gpt
GPT_PATH = config.get('DEFAULTS', 'beam.home') + '/bin/gpt' + util.getScriptExtension()
targetProductsPath = config.get('DEFAULTS', 'targetProductDir')
clearTargetProductsDir = config.getboolean('DEFAULTS', 'targetProductDir.clear')
if clearTargetProductsDir and os.path.exists(targetProductsPath):
    util.removeDir(targetProductsPath)           

time = datetime.datetime.utcnow()
resultFileName = 'Result_' + time.strftime("%Y%m%d-%H%M%S") + '.txt'    
resultsPath = os.getcwd() + '/results'
if not os.path.exists(resultsPath):
    os.makedirs(resultsPath)

csvWriter = csv.writer(open(resultsPath + '/' + resultFileName, 'w'), delimiter='\t')

graphConfigs = config.items("GRAPHS")

for config in graphConfigs:  
    runId = config[0]
    gptCommand = config[1]
    targetProductOption = "-t " + targetProductsPath + "/" + runId 
    cmd = GPT_PATH + " " + targetProductOption + " " + gptCommand
    
    t0 = datetime.datetime.utcnow()
    print("Starting [" + runId + "] at " + str(t0.time()))
    
    try:
        # TODO: Killing subprocess if started from IDE (Eclipse) does not work?
        process = subprocess.Popen(cmd)       
        process.wait()
    except SystemExit:
        process.terminate()

    t1 = datetime.datetime.utcnow()
    delta = t1 - t0
    output = [runId, delta, gptCommand]
    csvWriter.writerow(output)
    print("[" + runId + "] took: " + str(delta)) 
    if clearTargetProductsDir:
        util.removeDir(targetProductsPath)
        os.makedirs(targetProductsPath)
        
print('FINISHED')
