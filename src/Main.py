import os
import datetime
import subprocess
import util
import csv
import ConfigParser 

config = ConfigParser.ConfigParser()
config.read('testbed.config')

GPT_PATH = config.get('general', 'beam.home') + '/bin/gpt' + util.getScriptExtension()
targetProductsPath = config.get('general', 'targetProductDir')
graphConfigs = config.items("graphs")

        
clearTargetProductsDir = config.getboolean('general', 'targetProductDir.clear')
if clearTargetProductsDir and os.path.exists(targetProductsPath):
    util.removeDir(targetProductsPath)           

time = datetime.datetime.utcnow()
resultFileName = 'Result_' + time.strftime("%Y%m%d-%H%M%S") + '.txt'    
resultsPath = os.getcwd() + '/results'
if not os.path.exists(resultsPath):
    os.makedirs(resultsPath)

csvWriter = csv.writer(open(resultsPath + '/' + resultFileName, 'w'), delimiter='\t')

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
    output = [runId, delta, cmd]
    csvWriter.writerow(output)
    print("[" + runId + "] took: " + str(delta)) 
    if clearTargetProductsDir:
        util.removeDir(targetProductsPath)
        os.makedirs(targetProductsPath)
print('FINISHED')
