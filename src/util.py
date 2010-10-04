
import sys
import os
import string

PID_PREFIX_WINDOWS = "win"
PID_PREFIX_MACOSX = "darwin"

def getScriptExtension():
    platformIdentifier = sys.platform
    if platformIdentifier.startswith(PID_PREFIX_WINDOWS) :
        return ".bat"
    elif platformIdentifier.startswith(PID_PREFIX_MACOSX) :
        return ".command"    
    else:
        return ".sh"

def getTestbedProperties(propertyFile) :
    f = open(propertyFile)
    dictionary = {"":""}
    for line in f.readlines():  
        line = line.strip()
        if len(line) == 0: 
            continue
        
        keyValue = line.split('=')        
        dictionary.update({keyValue[0].strip() : keyValue[1].strip()})
        
    return dictionary

def removeDir(dirPath) :
    if not os.path.exists(dirPath):
        return;
    
    for name in os.listdir(dirPath):
        file = os.path.join(dirPath, name)
        if not os.path.islink(file) and os.path.isdir(file):
            removeDir(file)
        else:
            os.remove(file)
    os.rmdir(dirPath)
    return
