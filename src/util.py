
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

def getSectionMerely(config, sectionName):
    "returns the elements of the section specified by sectionName without the elements of the 'DEFAULT' section"
    default = config.items('DEFAULT')
    section = config.items(sectionName)
    for item in default:
        section.remove(item)
    return section


def getPermutedOptions(options):
    if not options:
        return []
    optionList = []
    optionValues = options[0][1].split(',')
    optionName = options[0][0]
    tailOptionList = getPermutedOptions(options[1:])
    for v in optionValues :
        if v.find('#') >= 0:
            valueList = v.split('#');
            cmdValue = valueList[0].strip()
            outputValue = valueList[1].strip()
        else :
            cmdValue = v.strip()
            outputValue = cmdValue
            
        if tailOptionList:
            for t in tailOptionList :
                currentOption = {optionName : [cmdValue, outputValue]}
                currentOption.update(t)
                optionList.append(currentOption)
        else:
            currentOption = {optionName : [cmdValue, outputValue]}
            optionList.append(currentOption)
                
           
    return optionList
