import os
import glob
import sys, stat
import re
import pdb
import time
##Creates the TextList
##Preconditions:
#   fileTxt - the Buildlog.txt
def createTextList(fileTxt):
    print("Creating TextList"+"....", end="", flush=True)
    filename = fileTxt
    lines = [line for line in open(filename)]
    os.chmod(filename, 0o777)
    F = open(filename, "w")
    ## keeps creating new lines on repeat##
    ##checks for duplicates and puts a \n on it
    for i in range(len(lines)):
       for j in range(i, len(lines)):
           #print (lines[i])
           if lines[i] == lines[j] and i != j:
               lines[i] = ''
       if lines[i] != '':
           F.write(''.join([lines[i], '\n']))
       F.flush()
    F.close()
    # flipping the list is necessary to clean assigned data type
    lines = lines[::-1]

    # remove this once finished with project, it's only for readability
    newfilename = "BuildLog1.txt"
    F = open(newfilename, "w")
    for i in lines:
        F.write(i)
        F.flush()
    F.close()
    print( "[Complete]")
    return lines

## main call function to fix all the errors
def fixAllErrors(fileLoc, fileList):
    initTime = time.time()
    fixError6278(fileList, fileLoc)
    fixError6362_7319(fileList, fileLoc)
    fixError6222(fileList, fileLoc)
    fixError6418(fileList, fileLoc)
    fixError6158(fileList, fileLoc)
    fixError6404(fileList, fileLoc)
    fixError6239(fileList, fileLoc)
    fixError6401(fileList, fileLoc)
    fixError6186(fileList, fileLoc)
    print("Time taken by functions: " + str(time.time()- initTime) +"s")

## this implicit statement is not positioned correctly within the scope
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6278(txtLines, fileLocation):
    print("Fixing error:6278 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
        A = txtLines[i]
        FindIndex4 = A.find("error #6278")
        if FindIndex4 != -1:
            LeftIndex2 = A.rfind("\\")
            RightIndex2 = A.rfind("(")
            newfilename = A[LeftIndex2+1:RightIndex2]
            print ("6278:" + newfilename)
            newfilename = fileLocation + newfilename

            LeftIndex3 = A.rfind("(")
            RightIndex3 = A.rfind(")")
            FileLine = A[LeftIndex3+1:RightIndex3]
            os.chmod(newfilename, 0o777)
            VarLine = int(FileLine)-1
            lines4 = [line4 for line4 in open(newfilename)]

            for ii in range(VarLine):
                if "IMPLICIT NONE" in lines4[ii]:
                    Index4 = ii

            F = open(newfilename, 'w')

            for iii in range(len(lines4)):
                if iii == Index4:
                    F.write("")
                    F.flush()
                elif iii == VarLine:
                    F.write(lines4[iii])
                    F.flush()
                    F.write("      IMPLICIT NONE\n")
                    F.flush()
                else:
                    F.write(lines4[iii])
                    F.flush()
            F.close()
    print( "[Complete]")

# Error error #6362: The data types of the argument(s) are invalid.
# error : 7319 This argument's data type is incompatible with this intrinsic procedure; procedure assumed
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6362_7319(txtLines, fileLocation):
    print("Fixing error:6362_7319 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex2 = A.find("error #6362")
       FindIndex3 = A.find("error #7319")

       if FindIndex2 != -1 or FindIndex3 != -1:
           LeftIndex1 = A.find("[")
           RightIndex1 = A.find("]")
           Var = A[LeftIndex1+1:RightIndex1]

           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.find("(")
           newfilename = fileLocation + A[LeftIndex2+1:RightIndex2]
           print ("6362/7319:" + newfilename)
           os.chmod(newfilename, 0o777)

           lines6 = [line6 for line6 in open(newfilename)]
           F = open(newfilename, 'w')

           for ii in range(len(lines6)):
               if 'REAL '+Var in lines6[ii] or 'INTEGER '+Var in lines6[ii]:
                   F.write("\n")
                   F.flush()
               else:
                   F.write(lines6[ii])
                   F.flush()
           F.close()
    print( "[Complete]")

#error #6222: This IMPLICIT statement is not positioned correctly within the scoping unit.
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6222(txtLines, fileLocation):
    print("Fixing Error:6222 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex2 = A.find("error #6222")

       if FindIndex2 != -1:
           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.rfind("(")
           newfilename = A[LeftIndex2+1:RightIndex2]
           print ("6222:" + newfilename)
           LeftIndex3 = A.rfind("(")
           RightIndex3 = A.rfind(")")
           FileLine = A[LeftIndex3+1:RightIndex3]

           os.chmod(newfilename, 0o777)

           lines7 = [line7 for line7 in open(NewFileName)]
           VarLine = int(FileLine)-1
           F = open(NewFileName, 'w')

           for ii in range(len(lines7)):
               if ii == VarLine and ("IMPLICIT NONE" in lines7[ii] or "IMPLICIT      NONE" in lines7[ii]):
                   F.write("\n")
                   F.flush()
               else:
                   F.write(lines7[ii])
                   F.flush()
           F.close()
    print( "[Complete]")

##This name has already been assigned a data type
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6418(txtLines, fileLocation):
    print("Fixing Error:6418 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex2 = A.find("error #6418")
       if FindIndex2 != -1:
           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.rfind("(")
           NewFileName = fileLocation+ A[LeftIndex2+1:RightIndex2]

           LeftIndex3 = A.rfind("(")
           RightIndex3 = A.rfind(")")
           FileLine = A[LeftIndex3+1:RightIndex3]
           # NewFileName = fileLocation + NewFileName
           # print ("6418:" + NewFileName)
           os.chmod(NewFileName, 0o777)
           VarLine = int(FileLine)-1
           if NewFileName.endswith('.f') or NewFileName.endswith('.for'):
    ##        if NewFileName  == "solve_udc_moon.f":
               lines2 = [line2 for line2 in open(NewFileName)]
               F = open(NewFileName, 'w')

               for ii in range(len(lines2)):
                   if ii != VarLine:
                       F.write(lines2[ii])
                       F.flush()
                   elif "real" in lines2[ii].lower() or "integer" in lines2[ii].lower():
                       if "," in lines2[ii]:
                           F.write(lines2[ii])
                           F.flush()
                       else:
                           F.write("C This line was deliberately left commented\n")
                           F.flush()
                   else:
                       F.write(lines2[ii])
                       F.flush()
               F.close()
    print( "[Complete]")

# implicit reference error
# The structure-name is invalid or is missing.
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6158(txtLines, fileLocation):
    print("Fixing Error:6158 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex2 = A.find("error #6158")

       if FindIndex2 != -1:

           LeftIndex1 = A.find("[")
           if LeftIndex1 != -1:
               RightIndex1 = A.find("]")
               Var = A[LeftIndex1+1:RightIndex1]

               LeftIndex2 = A.rfind("\\")
               RightIndex2 = A.rfind("(")
               NewFileName = fileLocation + A[LeftIndex2+1:RightIndex2]
               print ("6158: " + NewFileName)

               os.chmod(NewFileName, 0o777)
               lines6 = [line6 for line6 in open(NewFileName)]
               F = open(NewFileName, 'w')

               for ii in range(len(lines6)):
                   if 'REAL '+Var in lines6[ii] or 'INTEGER '+Var in lines6[ii]:
                       F.write("\n")
                       F.flush()
                   else:
                       F.write(lines6[ii])
                       F.flush()
               F.close()
    print( "[Complete]")
# IndexList = []
# VarList = ''
# FileList = ''

##This name does not have a type, and must have an explicit type.
##doesnt work with old buildlog, the swiparse.f is not sync'd with the buildlog
## Issues :
#       some duplicates when running the subroutine more than once - should be fixed 7/03/2020
##      duplicates the # of times the error in the file is called in buildlog
## fixs the above error
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6404(txtLines, fileLocation):
    print("Fixing Error:6404 " + "....", end="", flush=True)
    IndexList = []
    VarList = ''
    FileList = ''

    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex = A.find("error #6404")
       if FindIndex != -1:
           ## this segment isolates the buildlog variable
           LeftIndex1 = A.find("[")
           RightIndex1 = A.find("]")
           Var = A[LeftIndex1+1:RightIndex1]

           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.rfind("(")
           NewFileName = fileLocation + A[LeftIndex2+1:RightIndex2]

           LeftIndex3 = A.rfind("(")
           RightIndex3 = A.rfind(")")
           FileLine = A[LeftIndex3+1:RightIndex3]
           # NewFileName = "tsatv6 - backup\\" + NewFileName
           print ("6404:" + NewFileName)

           os.chmod(NewFileName, 0o777)
           VarLine = int(FileLine)-1
           # print ( VarLine)
           if NewFileName.endswith('.f') or NewFileName.endswith('.for'):
               lines2 = [line2 for line2 in open(NewFileName)]

               ## last known instance of index
               ImplicitNoneIndex = 0
               for ii in range(VarLine):
                   if 'IMPLICIT NONE' in lines2[ii]:
                       if lines2[ii][0] == ' ':
                           ImplicitNoneIndex = ii

               IncludeIndex = 0
               for ii in range(VarLine):
                   if 'INCLUDE' in lines2[ii] and ('.INS' in lines2[ii] or '.ins' in lines2[ii]):
                       if lines2[ii][0] == ' ':
                           IncludeIndex = ii

               SubroutineIndex = 0
               for ii in range(VarLine+1):
                   if 'SUBROUTINE' in lines2[ii]:
                       if lines2[ii][0] == ' ':
                           SubroutineIndex = ii

                ## if subroutine is lower than implicit, recount implicit
               if SubroutineIndex > ImplicitNoneIndex:
                   ImplicitNoneIndex = 0
                   for ii in range(len(lines2)-1, VarLine, -1):
                       if 'IMPLICIT NONE' in lines2[ii]:
                           if lines2[ii][0] == ' ':
                               ImplicitNoneIndex = ii

                   SubroutineIndex = len(lines2)-1
                   for ii in range(len(lines2)-1, VarLine, -1):
                       if 'SUBROUTINE' in lines2[ii]:
                           if lines2[ii][0] == ' ':
                               SubroutineIndex = ii

                   IncludeIndex = 0
                   for ii in range(SubroutineIndex):
                       if 'INCLUDE' in lines2[ii] and ('.INS' in lines2[ii] or '.ins' in lines2[ii]):
                           if lines2[ii][0] == ' ':
                               IncludeIndex = ii

               # print ( str(ImplicitNoneIndex) + " " + str(IncludeIndex)+ " " + str(SubroutineIndex) )
               if ImplicitNoneIndex<IncludeIndex:
                   Index = IncludeIndex
               else:
                   Index = ImplicitNoneIndex

               IndexList.append(Index)
               VarList = VarList+' '+Var
               if FileList:
                   FileList = FileList+','+NewFileName
               else:
                   FileList = NewFileName
               # print ("Index: " + str(Index))
           elif NewFileName.endswith('.ins') or NewFileName.endswith('.INS'):
               with open(NewFileName, "r+") as F:
                   old = F.read()
                   F.seek(0)
                   if (Var[0]>='I' and Var[0]<='N') or (Var[0]>='i' and Var[0]<='n'):
                       F.write("      INTEGER " + Var + '\n' + old)
                   else:
                       F.write("      REAL " + Var + '\n' + old)
               F.close()

    VarList = VarList.split()
    FileList = FileList.split(",")

    ##Stripped variables (filename, variable, variable index) from the buildlog are placed into their relative positions
    for i in range(len(IndexList)):
       NewFileName = FileList[i]
       Index = IndexList[i]
       Var = VarList[i]
       os.chmod(NewFileName, 0o777)
       lines3 = [line3 for line3 in open(NewFileName)]

       F = open(NewFileName, 'w')

       for ii in range(len(lines3)):
           # reprint the lines that don't need to be reworked
           if ii != Index:
               F.write(lines3[ii])
               F.flush()
           # reprint the lines and then write INTEGER VARIABLE on a single line
           #
           elif ii == Index and Var not in lines3[ii]:
               # print(lines3[ii])
               F.write(lines3[ii])
               F.flush()
               if (Var[0]>='I' and Var[0]<='N') or (Var[0]>='i' and Var[0]<='n'):
                   F.write("      INTEGER " + Var + '\n')
                   F.flush()
               else:
                   F.write("      REAL " + Var + '\n')
                   F.flush()
           # else:
           #     F.write(lines3[ii])
           #     F.flush()
           #     if (Var[0]>='I' and Var[0]<='N') or (Var[0]>='i' and Var[0]<='n'):
           #         F.write("      INTEGER " + Var + '\n')
           #         F.flush()
           #     else:
           #         F.write("      REAL " + Var + '\n')
           #         F.flush()
           #     print(Var)
       F.close()
    print( "[Complete]")

## fixs the Variable with Integer or real
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6239(txtLines, fileLocation):
    print("Fixing Error:6239 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
       A = txtLines[i]
       FindIndex = A.find("error #6239")
       if FindIndex != -1:
           LeftIndex1 = A.find("[")
           RightIndex1 = A.find("]")
           Var = A[LeftIndex1+1:RightIndex1]

           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.rfind("(")
           NewFileName = A[LeftIndex2+1:RightIndex2]
           print ("error6239: " + NewFileName)
           NewFileName = fileLocation + NewFileName

           if NewFileName.endswith('.ins') or NewFileName.endswith('.INS'):
               with open(NewFileName, "r+") as F:
                   old = F.read()
                   F.seek(0)
                   if (Var[0]>='I' and Var[0]<='N') or (Var[0]>='i' and Var[0]<='n'):
                       F.write("      INTEGER " + Var + '\n' + old)
                   else:
                       F.write("      REAL " + Var + '\n' + old)
               F.close()
    print( "[Complete]")

# error #6401: The attributes of this name conflict with those made accessible by a USE statement.
#find library and put ",ONLY: VARNAME1, VARNAME2" on the use statement
#It works, but probably not needed
#flaws: it adds ONLY: to all the use modules that has that variable from buildlog. Could be better optimized. - 7/15/2020
def fixError6401(txtLines, fileLocation):
    print("Fixing Error:6401 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
        A = txtLines[i]
        # findUse = A.find("      use ")
        findIndex = A.find("error #6401")
        if findIndex != -1:
           LeftIndex1 = A.find("[")
           RightIndex1 = A.find("]")
           Var = A[LeftIndex1+1:RightIndex1]

           LeftIndex2 = A.rfind("\\")
           RightIndex2 = A.rfind("(")
           NewFileName = A[LeftIndex2+1:RightIndex2]
           LeftIndex3 = A.rfind("(")
           RightIndex3 = A.rfind(")")
           FileLine = A[LeftIndex3+1:RightIndex3]

           print ("error6401: " + NewFileName)
           NewFileName = fileLocation + NewFileName
           os.chmod(NewFileName, 0o777)

           lines8 = [line8 for line8 in open(NewFileName)]
           varLine = int(FileLine) -1
           F = open(NewFileName, 'w')
           for ii in range(len(lines8)):
               if ii == varLine:
                   lines8[ii] = "C This line was deliberately left commented\n"
               if 'use' in lines8[ii].lower():
                   libraryContainsVar= ""
                   LeftIndex4 = lines8[ii].lower().rfind("use ")
                   RightIndex4 = lines8[ii].rfind("\n")
                   useLibraryVar = lines8[ii][LeftIndex4+4:RightIndex4]

                   ## if there is a space in useLibrary, the line is a comment, ignore the line
                   if ' ' in useLibraryVar and "ONLY:" not in useLibraryVar:
                       F.write(lines8[ii])
                       F.flush()
                       continue
                   elif ' ' in useLibraryVar and "ONLY: " in useLibraryVar:
                       RightIndex4 = lines8[ii].find(",")
                       useLibraryVar = lines8[ii][LeftIndex4+4:RightIndex4]

                   libraryFileName = fileLocation + useLibraryVar + ".f90"
                   #check if useLibraryVar relates to the file
                   os.chmod(libraryFileName, 0o444)
                   lines9 = [line9 for line9 in open(libraryFileName)]
                   for iii in range(len(lines9)):
                       if Var.lower() in lines9[iii]:
                           libraryContainsVar = Var
                   newLine = lines8[ii]
                   if libraryContainsVar == Var and ( ", ONLY: " not in lines8[ii]):
                       newLine = lines8[ii].rstrip('\n')+ ", ONLY: " + libraryContainsVar + "\n"
                       F.write( newLine)
                       F.flush()
                   elif libraryContainsVar == Var and ", ONLY: " in lines8[ii] and (libraryContainsVar not in lines8[ii]):
                       newLine = lines8[ii].rstrip('\n')+ ", " + Var + "\n"
                       F.write( newLine)
                       F.flush()
                   else:
                       F.write(newLine)
                       F.flush()
               else:
                   F.write(lines8[ii])
                   F.flush()
           F.close()
    print( "[Complete]")
## fixs format function descriptor. invalid format descriptors are removed.
##Precondition:
##  txtLines - the BuildLog.txt
##  fileLocation - file directory
def fixError6186(txtLines, fileLocation):
    print("Fixing error:6186 " + "....", end="", flush=True)
    for i in range(len(txtLines)):
        A = txtLines[i]
        findIndex = A.find("error #6186")

        if findIndex != -1:
            LeftIndex1 = A.rfind("\\")
            RightIndex1 = A.rfind("(")
            newfilename = A[LeftIndex1+1:RightIndex1]
            print ("6186: " + newfilename)
            newfilename = fileLocation + newfilename

            LeftIndex2 = A.rfind("(")
            RightIndex2 = A.rfind(")")
            FileLine = A[LeftIndex2+1:RightIndex2]

            LeftIndex3 = A.rfind("[")
            RightIndex3 = A.rfind("]")
            Var = A[LeftIndex3+1:RightIndex3]

            os.chmod(newfilename, 0o777)
            VarLine = int(FileLine)-1
            lines11 = [line11 for line11 in open(newfilename)]

            F = open(newfilename, 'w')

            for ii in range(len(lines11)):
                if ii == VarLine:
                    F.write(re.sub(r'\b%s\b' %Var, '', lines11[ii]))
                    F.flush()
                else:
                    F.write(lines11[ii])
                    F.flush()
            F.close()
    print( "[Complete]")
