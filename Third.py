import os, os.path
import re
import glob
import time
from collections import namedtuple
# import time
# reservedIdentifier = ['INTRINSIC','COMMON','EQUIVALENCE', 'COMPLEX', 'DATA', 'LOGICAL', 'INTEGER', 'DOUBLE', 'PRECISION', 'REAL', 'CHARACTER', \
#     'EXTERNAL', 'TYPE', 'DIMENSION', 'SAVE', 'RECORD', 'STRUCTURE']
## Placed the most occuring declared identifiers near the front of the list, EQUIVALENCE is omitted because of how the storage logic is used
reservedIdentifier = ['INTEGER', 'REAL', 'CHARACTER', 'DIMENSION', 'SAVE', 'LOGICAL', 'DATA' 'INTRINSIC','COMMON', 'COMPLEX', \
    'DOUBLE', 'PRECISION', 'EXTERNAL', 'TYPE','RECORD', 'STRUCTURE']
IMPLICIT_NONE_REGEX = re.compile(r'\bIMPLICIT\sNONE\b', re.I)
FILE_REGEX = re.compile(r'.*\.(f|for|ins)\b', re.I)
CONT_REGEX = re.compile(r'^ {5}\S', re.I)
MyVarList = namedtuple('MyVarlist', 'index, name, type')

## localFileVariableCleanUp
##  -reorganizes the section of variables into a single categorized list
##  -issues: should not call function twice, it has a sideeffect of removing some variable declarations if repeated twice
##Precondition:
##  fileLocation - file directory
def localFileVariableCleanUp(fileDir):
    files = [file for file in os.listdir(fileDir) if FILE_REGEX.search(file)]
    print("Realigning local file variables (" +str(len(files))+" files)....\n", end="", flush=True)
    initTime = time.time()
    for filename in files:
        print("\t" + filename +"\n", end="", flush=True)
        implicitIndex = 0
        implicitList = []
        varString = ''
        varDict = {}
        tempDict = {}
        postVarList = []
        tmpIdentifier = ''
        contIdentifer = ''

        os.chmod(fileDir+filename, 0o777)
        lines = [line for line in open(fileDir+filename)]
        F = open(fileDir+filename, 'w')
        ## First pass finds all the declared variables and assigns it into a dictionary MyVar(index, var name, type)
        for i in range(len(lines)):
            if "      IMPLICIT NONE" in lines[i].upper():
                implicitList.append(i)
                varDict[i] = MyVarList(i, '', 'IMPLICIT NONE')
            elif i == len(lines)-1:
                implicitList.append(i)
                varDict[i] = MyVarList(i, '', 'IMPLICIT NONE')
            if contIdentifer != '' and CONT_REGEX.search(lines[i]):
                contVarMatch = re.search(r'\b.*', lines[i])
                if contVarMatch.group(0).endswith(','):
                    varDict[i] = MyVarList(i, contVarMatch.group(0)[:-1], contIdentifer)
                else:
                    varDict[i] = MyVarList(i, contVarMatch.group(0), contIdentifer)
            else:
                contIdentifer = ''
            for ii in reservedIdentifier:
                if ' :: ' not in lines[i]:
                    varMatch = re.search(r'^ {6}%s\*?\d*\b' %ii, lines[i].upper())
                if varMatch:
                    # if 'COMMON' in varMatch.group(0):
                    #     varMatch = re.search(r' {6}\w*( \/\w*\/)?', lines[i].upper())
                    # varList.append(MyVarList(i, lines[i][len(varMatch.group(0))+1:-1], varMatch.group(0)))
                    if lines[i][:-1].endswith(','):
                        varDict[i] = MyVarList(i, lines[i][len(varMatch.group(0))+1:-2], varMatch.group(0))
                        contIdentifer = varMatch.group(0)
                    else:
                        varDict[i] = MyVarList(i, lines[i][len(varMatch.group(0))+1:-1], varMatch.group(0))
                    break
        impCount = 0
        tempDict = varDict.copy()
        ##second pass organizes the variables into assigned groups.
        for j in range(len(lines)):
            if j in varDict:
                if 'IMPLICIT NONE' in varDict[j][2]:
                    if implicitList[impCount] == j:
                        impCount += 1
                    F.write(lines[j])
                    F.flush()
                else:
                    varString = varDict[j][2] + ' '
                    varSum = len(varDict[j][2]) + 1
                    if varDict[j][2] not in postVarList:
                        postVarList.append(varDict[j][2])
                    for jj in dict(tempDict):
                        if len(implicitList) == 1:
                            implicitIndex = len(lines)
                        else:
                            # print(implicitList)
                            # print(filename)
                            implicitIndex = implicitList[impCount]
                        # print (implicitIndex)
                        if jj >= j and jj < implicitIndex and tempDict[jj][2] != 'IMPLICIT NONE' and varDict[j][2] == tempDict[jj][2]:
                        # if jj >= j  and tempDict[jj][2] != 'IMPLICIT NONE' and varDict[j][2] == tempDict[jj][2]:
                            varSum += len(tempDict[jj][1]) + 1
                            if varSum < 72:
                                varString += tempDict[jj][1] + ','
                            else:
                                if jj != list(tempDict)[-1]:
                                    varSum = len('     &')+len(tempDict[jj][1])+1
                                    varString += '\n' + '     &' +tempDict[jj][1] + ','
                                else:
                                    varString += '\n' + '     &' +tempDict[jj][1]
                            tmpIdentifier = tempDict[jj][2]
                            del tempDict[jj]
                    while varString.endswith(','):
                        varString = varString[:-1]
                    # print (tempDict)
                    # print (len(tmpIdentifier))
                    # print (len(varString[:-1]))
                    if varString[:-1] not in postVarList:
                        # print (varString)
                        F.write(varString)
                        F.flush()
                        F.write('\n')
                        F.flush()
            else:
                F.write(lines[j])
                F.flush()
        F.close()
    print("Time taken by function: " + str(time.time()- initTime) +"s")
    print( "[Complete]")
