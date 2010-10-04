import os
import datetime
import subprocess
import util
import csv

 
props = util.getTestbedProperties(os.getcwd() + '/testbed.properties')
GPT_PATH = props['beam.home'] + '/bin/gpt' + util.getScriptExtension() 
graph = '"' + os.getcwd() + '/' + props['graph'] + '"'

#sourceProduct = '-Ssource=' + '"C:\\Dokumente und Einstellungen\\Marco Peters\\Eigene Dateien\\EOData\\Meris\\FSG\\MER_FSG_1PNACR20030530_105441_000001772016_00452_06518_0000.N1"'
sourceProduct = '-Ssource=' + '"' + os.getcwd() + "/sourceProducts" + '/MER_RR__1PQBCM20040526_092957_000001012027_00122_11699_0148.N1"'

optionReader = csv.reader(open(os.getcwd() + '/gpt.options'), delimiter='\t')
gptOptionsList = []
for row in optionReader :
    optionName = row[0]
    optionValues = row[1:]
    options = []
    if len(optionValues) == 1 and len(optionValues[0]) == 0 :
        options.append(optionName)
        options.append("")
    else:
        for v in optionValues :
            options.append(optionName + " " + v)
            
    gptOptionsList.append(options)
    
print(gptOptionsList)

combinedOptions = gptOptionsList[0]
gptOptionsList = gptOptionsList[1:]

for opts in gptOptionsList :
    for cOptIndex in range(len(combinedOptions)):
        for oIndex in range(len(opts)) :
            combinedOptions.append(combinedOptions[cOptIndex] + " " + opts[oIndex])

        
print(combinedOptions)


for gptOpts in combinedOptions: 
    cmd = GPT_PATH + ' ' + graph + ' ' + gptOpts + ' ' + sourceProduct
    print(cmd)
    print("Starting Run [" + gptOpts + "]")
    t0 = datetime.datetime.utcnow()
    process = subprocess.Popen(cmd)
    process.wait()
    t1 = datetime.datetime.utcnow()
    delta = t1 - t0
    print("Run [" + gptOpts + "] took: ") 
    print(delta)
    
