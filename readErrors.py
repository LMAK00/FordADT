import os
import glob
import sys, stat
import re
import pdb
import time
##builds the BuildLog.txt
## currently works with 6278,6222,6418,
def buildTxtFile(fileText, fileLocation):
    F = open(fileText, "w")
    F.write("BuildLog for Fortran Converter \nCompiling with Intel(R) Visual Fortran Compiler 19.0.5.281 \n")
    F.flush()
    #calling all findErrors
    print ("Checking for errors:")
    # initTime = time.time()
    for filename in glob.iglob(fileLocation + "*.f*"):
        if filename.endswith('.f') or filename.endswith('.for') or filename.endswith('.f90'):
            findError6186(filename, fileText)
            findError6222(filename, fileText)
            findError6278(filename, fileText)
            findError6418(filename, fileText)
            if not filename.endswith('*.f') and not '.f90' in filename:
                findError6404(filename, fileText, fileLocation)

            # TESTING SINGLE FILES
            # if 'readdsa.f' in filename:
            #     findError6404(filename, fileText, fileLocation)
                # findError6186(filename, fileText)
    # print("Time taken by functions: " + str(time.time()- initTime) +"s")
    F.close()

#works! 12:42pm
## Finds if the implicit statement is positioned incorrectly, if it is then add to the build log
## Preconditions:
##  fileName - the file to be read
##  errorFile - the buildlog file
def findError6278(fileName, errorFile):
    print("Error:6278 " + fileName +"....", end="", flush=True)
    F = open(errorFile, 'a')
    os.chmod(errorFile, 0o777)
    newFileName = fileName
    os.chmod(newFileName, 0o777)
    lines4 = [line4 for line4 in open(newFileName)]
    commentSet = ['c','C','d','D','!','*']
    identifiers= ['LOGICAL', 'REAL', 'INTEGER']
    useIndex = 0
    implicitIndex = 0
    subroutineIndex = 0

    for i in range(len(lines4)):
        if lines4[i][0] in commentSet or lines4[i] == '\n':
            continue
        ## '*' for the commented file
        if "      USE " in lines4[i].upper() and "*" not in lines4[i]:
            useIndex = i
        elif "      IMPLICIT NONE" in lines4[i].upper():
            implicitIndex = i
        #resets the index counters and checks for error6278
        if "      SUBROUTINE" in lines4[i].upper() or (" FUNCTION " in lines4[i].upper() and ' FORMAT(' not in lines4[i].upper()):
            if (useIndex > implicitIndex) and (implicitIndex != subroutineIndex):
                # print ("Use:" + str(useIndex) + ", implicit: " + str(implicitIndex) + ', subr '+ str(subroutineIndex))
                F.write(newFileName + "(" + str(implicitIndex) + "): error #6278 \n")
                F.flush()
            useIndex = i
            implicitIndex = i
            subroutineIndex = i
    F.close()
    print( "[Complete]")

# #needs the variable line with function and no declaration
# # variable without ()
# # variable without TBLOPT =  <--- spacing
## Don't have a working version
# def findError6362(fileName, errorFile):
#     F = open(errorFile, 'a')
#     os.chmod(errorFile,0o777)
#     newFileName = fileName
#     os.chmod(newFileName, 0o444)
#
#     lines6 = [line6 for line6 in open(newFileName)]
#     lines6 = lines6[::-1]
#
#     varList = []
#
#     assignIndex = 0
#     for i in range(len(lines6)):
#         if "=" in lines6[i]:
#             assignIndex = lines6[i].find("=")
#         if "      SUBROUTINE" in lines6[i]:
#             #clear the varList
#             print ("!")
#     F.close()

# ##warning #7319: This argument's data type is incompatible with this intrinsic procedure; procedure assumed EXTERNAL.
# def findError7319(fileName, errorFile):
#     F = open(errorFile, 'a')
#     os.chmod(errorFile,0o777)
#     newFileName = fileName
#     os.chmod(newFileName, 0o444)
#
#     lines7 = [line7 for line7 in open(newFileName)]
#
#     varList = []
#
#     for i in range(len(lines7)):
#         if


#should work, its probably covered by error 6278, so not needed
## Preconditions:
##  fileName - the file to be read
##  errorFile - the buildlog file
def findError6222(fileName, errorFile):
    print("Error:6222 " + fileName +"....", end="", flush=True)
    F = open(errorFile, 'a')
    os.chmod(errorFile,0o777)
    newFileName = fileName
    os.chmod(newFileName, 0o777)

    lines7 = [line7 for line7 in open(newFileName)]
    for i in range(len(lines7)):
        if ("implicit " in lines7[i].lower() and ("none" not in lines7[i].lower()) and (lines7[i][0:1].find("C") == -1) and (lines7[i][0:1].find("*") == -1)):
            F.write(newFileName + "(" + str(i+1) + "): error #6222 \n")
            F.flush()
    F.close()
    print("[Complete]")

## need exception case for INTEGER*4 LTRANC, INTEGER*2 LTRANC
## or take entire variable with Identifier
## for duplicate variable declarations
## Preconditions:
##  fileName - the file to be read
##  errorFile - the buildlog file
def findError6418(fileName, errorFile):
    print("Error:6418 " + fileName +"....", end="", flush=True)
    if not fileName.endswith('.f90'):
        F = open(errorFile, 'a')
        os.chmod(errorFile,0o777)
        newFileName = fileName
        os.chmod(newFileName, 0o777)

        lines2 = [line2 for line2 in open(newFileName)]

        checkValues = False

        # lines2 = lines2[::-1]
        varList = []
        #list of reserved words from Fortran
        reservedList = ['SUBROUTINE', 'DO', 'ENDDO', 'INQUIRE', 'ASSIGN', 'GO', 'WRITE', 'DATA',\
            'UNIT', 'OPENED', 'IF', 'ELSE', 'ELSEIF', 'EXIT', 'RETURN', 'ENDDO', 'FILE', 'ACTION', 'IOSTAT', 'READ', \
            'THEN', 'ENDIF', 'INTENT', 'CLOSE', 'PROGRAM', 'ERR', 'CASE', 'ALLOCATABLE', 'REALLOCATE', 'POINTER', 'SELECT CASE', 'PARAMETER', 'IMPLICIT', \
            'CASE DEFAULT' , 'SELECT' , 'DIMENSION', 'CONTINUE', 'NUMBER', 'WRITE', 'END', 'FORMAT', 'CALL', \
            'REC', 'LEN', 'SAVE', 'ENTRY', 'GOTO', 'ALLOCATE', 'DEALLOCATE', 'TYPE']
        reservedIdentifier = ['COMMON', 'AUTOMATIC', 'EQUIVALENCE', 'COMPLEX', 'LOGICAL', 'INTEGER', 'REAL', 'CHARACTER', 'EXTERNAL' , '+', '&', 'INCLUDE']
        ##mostly for catching inline functions, hotfix
        reservedSpecialCase = ['GETSWB', 'DDAT', 'REALI', 'STAT', 'AIMAG','NMLINE', 'SSYSA', 'XPD', 'III', 'ANYNEW_GET']
        ##create new list by replacing all symbols with commas
        for i in range(len(lines2)):
            newLine = lines2[i]

            #removes the nested brackets, better to implement with stacks
            pushBracket = 0
            popBracket = 0
            hasBracket = newLine.find(")")
            while (hasBracket != -1):
                for ii in range(0, len(newLine)):
                    if "(" in newLine[ii]:
                        pushBracket = ii
                    elif ")" in newLine[ii]:
                        popBracket = ii
                        newLine = newLine[0:pushBracket] + newLine[popBracket+1::]
                        break
                    elif newLine.endswith(',') and ")" not in newLine:
                        newLine = newLine[0,pushBracket]
                        hasBracket = -1
                        break
                if newLine.find(")") == -1:
                    hasBracket = -1
            ## remove inline comments
            if "!" in newLine:
                newLine = newLine[:newLine.find("!")]
            ## if any of the values are not within "a-zA-Z0-9 \n . _" then replace with commas
            newLine = re.sub('[^a-zA-Z0-9\n\.\_]', ',', newLine.strip())
            while(newLine.startswith(',')):
                newLine = newLine[1::]
            while(newLine.endswith(',')):
                newLine = newLine[0:len(newLine)-1]
            ##if file has lowercases, change lines to upper
            newLine = newLine.upper()
            # print (newLine)
            ## check if it's a declaration
            if newLine.startswith("REAL") or newLine.startswith("INTEGER"):
                LeftIndex4 = 0
                RightIndex4 = 0
                # sorts all the variables in between the commas
                # ex.   GSRCD,BASPC
                #       INTEGER,ISTN2,ITFK,IZONE,IBARK,KK,JBSTAJ,I2,I,J,K
                while(LeftIndex4 != -1):
                    if "C" in lines2[i][0] or "*" in lines2[i][0] or "!" in lines2[i][0] or newLine =='':
                            break
                    if(LeftIndex4 == RightIndex4):
                        RightIndex4 = newLine.find(',')
                    elif (LeftIndex4 != -1 and RightIndex4 == -1):
                        RightIndex4 = len(newLine)
                    else:
                        if LeftIndex4 == 0:
                            varList.append(newLine[LeftIndex4:RightIndex4])
                            if not newLine[LeftIndex4:RightIndex4] in reservedList and \
                                not newLine[LeftIndex4:RightIndex4] in reservedIdentifier and \
                                not newLine[LeftIndex4:RightIndex4] in reservedSpecialCase and \
                                not newLine[LeftIndex4:RightIndex4] in varList and \
                                newLine[LeftIndex4:RightIndex4].isidentifier():
                                    F.write(newFileName + "(" + str(i+1) + ") error #6418: [" + newLine[LeftIndex4:RightIndex4] + "] \n")
                                    F.flush()
                            LeftIndex4 = newLine.find(',')
                            RightIndex4 = newLine.find(',', LeftIndex4 + 1)
                        else:
                            ##if a variable such as someValue1,,someValue2 is called
                            ##                              ---^
                            if newLine[LeftIndex4+1:RightIndex4] != '':
                                ## if value is not any of the unique values, it's a variable
                                if newLine[LeftIndex4+1:RightIndex4] in varList and \
                                not newLine[LeftIndex4+1:RightIndex4] in reservedIdentifier and \
                                not newLine[LeftIndex4+1:RightIndex4] in reservedList and \
                                not newLine[LeftIndex4+1:RightIndex4] in reservedSpecialCase and \
                                newLine[LeftIndex4+1:RightIndex4].isidentifier():
                                    F.write(newFileName + "(" + str(i+1) + ") error #6418: [" + newLine[LeftIndex4+1:RightIndex4] + "] \n")
                                    F.flush()
                                else:
                                    varList.append(newLine[LeftIndex4+1:RightIndex4])
                            LeftIndex4 = newLine.find(',', LeftIndex4 + 1)
                            RightIndex4 = newLine.find(',', LeftIndex4 + 1)
            ##clear the variable List if finished running through the declaration block,
            ##may append one or two non-declaration variables, but no issues with it
            if "SUBROUTINE" in newLine or "FUNCTION" in newLine or "IF" in newLine or "END" in newLine:
                varList = []
        F.close()
    print("[Complete]")

    #need to check variables with () ex. LOADWID
    # maybe general case with use libraries only
    # try working with isidentifier()
def findError6158(fileName, errorFile):
    print("Error:6158 " + fileName +"....", end="", flush=True)
    print("[Complete]")

# checks if there is a invalid argument descriptor in the internal format function
## Preconditions:
##  fileName - the file to be read
##  errorFile - the buildlog file
def findError6186(fileName, errorFile):
    print("Error:6186 " + fileName+ "....", end="", flush=True)
    F = open(errorFile, 'a')
    os.chmod(errorFile,0o777)
    newFileName = fileName
    os.chmod(newFileName, 0o777)

    lines2= [line2 for line2 in open(newFileName)]

    isFormat = False
    isComment = False
    descriptorList= []
    tmpLine = ''

    DECLARE_FORMAT_REGEX = re.compile(r'[ ]?FORMAT[ ]*\({1}', re.I)
    FORMAT_REGEX = re.compile(r'[ ]*(?:[a-z_][a-z0-9_]*[ ]*:[ ]*)?')
    FORMAT_SPEC_REGEX = re.compile(r'\'[^,]*\'', re.I)
    COMMENT_REGEX = re.compile(r'\'[^,]*\'', re.I) # single comments w/o ,
    COMMENT_EXCLUDED_REGEX = re.compile(r'\'.*\'', re.I) #the entire comment w/ ,  \'.*\'
    COMMENT_OPEN_REGEX = re.compile(r'\'[^\')]+$', re.I)
    COMMENT_CLOSE_REGEX = re.compile(r'[^\']+\'', re.I)  #^[ ]{5}.*\'{1}
    FORMAT_CONT_REGEX = re.compile(r'^ {5}[^ ]{1}', re.I)
    FORMAT_END_REGEX = re.compile(r'.{5}.*\)$', re.I)
    FORMAT_DESCRIPT_REGEX2 = re.compile(r'\d*(TL|TR|BZ|BN|SP|SS|A|B|D|E|F|G|H|I|L|S|T|P|X|Z|0){1}\d*\.*\d*', re.I)
    FORMAT_DESCRIPT_REGEX = re.compile(r'\d*\w*\.?\d*', re.I)

    for i in range(len(lines2)):
        if re.search("^[cCdD!*]", lines2[i][0]) or lines2[i] == '\n':
            continue
        newLine = lines2[i]
        if DECLARE_FORMAT_REGEX.search(newLine):
            isFormat = True
        elif isFormat and not FORMAT_CONT_REGEX.search(newLine):
            isFormat = False
        if isFormat:
            newLine = re.sub(r'\'{2}', '', newLine)
            newLine = COMMENT_REGEX.sub('', newLine)
            if isComment:
                newLine = newLine[newLine.find('\'')+1:-1]
                isComment = False
            newLine = re.sub(r'.*FORMAT\b[ ]*', '      ', newLine, flags=re.I)
            newLine = FORMAT_CONT_REGEX.sub('', newLine) ##remove the continuation character
            if newLine.find('\'') != -1:
                newLine = COMMENT_EXCLUDED_REGEX.sub('', newLine)
                if newLine.count('\'') == 1:
                    newLine = COMMENT_OPEN_REGEX.sub('', newLine)
                    isComment = True
            for ii in FORMAT_DESCRIPT_REGEX.findall(newLine):
                if ii and re.fullmatch(r'\d*\.?\d*', ii, flags=re.I) is None:
                    descriptorList.append(ii)
            for iii in descriptorList:
                if not FORMAT_DESCRIPT_REGEX2.fullmatch(iii):
                    F.write(newFileName + "(" + str(i+1) + ") error #6186: [" + iii + "] \n")
                    F.flush()
            descriptorList = []
        else:
            continue
    F.close()
    print("[Complete]")

# assumption for only the general cases
## I to N --> INT
## OTHER  --> REAL
# checks if there is an undeclared variable in the file
## Preconditions:
##  fileName - the file to be read
##  errorFile - the buildlog file
##  fileLocation -
def findError6404(fileName, errorFile, fileLocation):
    print("Error:6404 " + fileName +"....", end="", flush=True)
    F = open(errorFile, 'a')
    os.chmod(errorFile,0o777)
    newFileName = fileName
    os.chmod(newFileName, 0o777)

    lines2 = [line2 for line2 in open(newFileName)]
    ## boolean check if it's the continuation of format function
    isFormat = False
    hasImplicit = False
    isSubroutine = False
    isFunction = False
    isDefined = False
    hasIdentifier = False
    ext_hasIdentifier = False
    hasQuote = False
    hasDblQuote = False
    initTime = time.time() ## COMMENT OUT LATER

    USE_REGEX = re.compile(r'[ ]*USE([, ]+INTRINSIC)?[ :]+([a-z0-9_]*)([, ]+ONLY[ :]+)?', re.I)
    INCLUDE_REGEX = re.compile(r'[ ]*INCLUDE[ :]*[\'\"]([^\'\"]*)', re.I)
    ## THIS CAN BE OPTIMIZED? 66 steps!
    LOGIC_REGEX = re.compile(r'\.\s*(LT|LE|GT|GE|AND|NOT|NEQV|XOR|OR|EQV|NE|EQ)\s*\.', re.I)
    ##\W\.*\s*(LT|LE|GT|GE|AND|NOT|OR|NEQV|XOR|EQV|NE|EQ)\s*\.* <--- expensive, but it will catch all extended line variables

    varList = []
    extendedVarList = []
    exList = []
    functionList = []
    prevVar = []
    ##used to storage the DO loop variable
    #list of reserved words from Fortran, interal functions
    ## # TODO: need to fix internal functions 5/24/2021 later on
    reservedList = ['DO', 'CYCLE', 'ENDDO', 'CONTAINS', 'INQUIRE', 'ASSIGN', 'GO', 'WRITE', 'DATA',\
        'UNIT', 'OPENED', 'IF', 'ELSE', 'ELSEIF', 'EXIT', 'RETURN', 'ENDDO', 'FILE', 'ACTION', 'IOSTAT', 'READ', \
        'THEN', 'ENDIF', 'CLOSE', 'PROGRAM', 'ERR', 'CASE', 'SELECT CASE', \
        'CASE', 'DEFAULT' , 'SELECT' , 'CONTINUE', 'NUMBER', 'GOTO', 'WRITE', 'END', 'FORMAT', 'CALL', \
        'REC', 'LEN', 'SAVE', 'ENTRY', 'STOP', 'GOTO', 'TO', 'ATAN', 'ATAN2', 'AIMAG', 'INCLUDE', 'ALLOCATE', 'DEALLOCATE', 'SUBROUTINE', 'TYPE', \
        'IMPLICIT', 'NONE', 'STAT', 'INDEX', 'REWIND','C']
    ### TODO: FUNCTION KEYS FROM NOTEPAD++, THIS SHOULD BE A THOROUGH LIST OF INTRINSIC FUNCTIONS
    ##        DOESNT HAVE ALL THE OBSOLETE FUNCTIONS SUCH AS INUM, JNUM, KNUM, ...
    reservedNotepadKey = ['__FILE__', '__LINE__', '__DATE__', '__TIME__', '__TIMESTAMP__', 'ABS', 'ACCESS', 'ACHAR', 'ACOS', 'ACOSD', 'ACTION', 'ADJUSTL', 'ADJUSTR', 'ADVANCE', 'AIMAG', 'AIMAX0', 'AIMIN0', 'AINT', 'AJMAX0', 'AJMIN0', 'AKMAX0', 'AKMIN0', 'ALL', 'ALLOCATABLE', 'ALLOCATE', 'ALLOCATED', 'ALOG', 'ALOG10', 'AMAX0', 'AMAX1', 'AMIN0', 'AMIN1', 'AMOD', 'ANINT', 'ANY', 'APOSTROPHE', 'ASIN', 'ASIND', 'ASSIGN', 'ASSIGNMENT', 'ASSOCIATE', 'ASSOCIATED', 'ASYNCHRONOUS', 'ATAN', 'ATAN2', 'ATAN2D', 'ATAND', 'BACKSPACE', 'BIND', 'BIT_SIZE', 'BITEST', 'BITL', 'BITLR', 'BITRL', 'BJTEST', 'BKTEST', 'BLANK', 'BLOCKDATA', 'BREAK', 'BTEST','CABS', 'CALL', 'CASE', 'CCOS', 'CDABS', 'CDABS', 'CDCOS', 'CDCOS', 'CDEXP', 'CDEXP', 'CDLOG', 'CDLOG', 'CDSIN', 'CDSIN', 'CDSQRT', 'CDSQRT', 'CEILING', 'CEXP', 'CHAR', 'CHARACTER', 'CLASS', 'CLOG', 'CLOSE', 'CMPLX', 'COMMON', 'COMPLEX', 'CONJG', 'CONTAINS', 'CONTINUE', 'COS', 'COSD', 'COSH', 'COTAN', 'COTAND', 'COUNT', 'CPU_TIME', 'CRITICAL', 'CSHIFT', 'CSIN', 'CSQRT', 'CYCLE', 'DABS', 'DACOS', 'DACOSD', 'DASIN', 'DASIND', 'DATA', 'DATAN', 'DATAN2', 'DATAN2D', 'DATAND', 'DATE', 'DATE_AND_TIME', 'DBLE', 'DCMPLX', 'DCMPLX', 'DCONJG', 'DCONJG', 'DCOS', 'DCOSD', 'DCOSH', 'DCOTAN', 'DCOTAN', 'DCOTAND', 'DDIM', 'DEALLOCATE', 'DECIMAL', 'DECODE', 'DEFAULT', 'DELIM', 'DEXP', 'DFLOAT', 'DFLOTI', 'DFLOTJ', 'DFLOTK', 'DIGITS', 'DIM', 'DIMAG', 'DIMAG', 'DIMENSION', 'DINT', 'DIRECT', 'DLL_EXPORT', 'DLL_IMPORT', 'DLOG', 'DLOG10', 'DMAX1', 'DMIN1', 'DMOD', 'DNINT', 'DO', 'DOT_PRODUCT', 'DOUBLE', 'DOUBLECOMPLEX', 'DOUBLEPRECISION', 'DOWHILE', 'DPROD', 'DREAL', 'DREAL', 'DSIGN', 'DSIN', 'DSIND', 'DSINH', 'DSQRT', 'DTAN', 'DTAND', 'DTANH', 'DVCHK', 'ELSE', 'ELSEIF', 'ELSEWHERE', 'ENCODE', 'ENCODING', 'END', 'ENDASSOCIATE', 'ENDBLOCKDATA', 'ENDCRITICAL', 'ENDDO', 'ENDENUM', 'ENDFILE', 'ENDFORALL', 'ENDFUNCTION', 'ENDIF', 'ENDINTERFACE', 'ENDMODULE', 'ENDPROCEDURE', 'ENDPROGRAM', 'ENDSELECT', 'ENDSUBMODULE', 'ENDSUBROUTINE', 'ENDTYPE', 'ENDWHERE', 'ENTRY', 'ENUM', 'EOR', 'EOSHIFT', 'EPSILON', 'EQUIVALENCE', 'ERR', 'ERRMSG', 'ERRSNS', 'EXIST', 'EXIT', 'EXP', 'EXPONENT', 'EXTERNAL', 'FILE', 'FIND', 'FLEN', 'FLOAT', 'FLOATI', 'FLOATJ', 'FLOATK', 'FLOOR', 'FLUSH', 'FLUSH', 'FMT', 'FORALL', 'FORM', 'FORMAT', 'FORMATTED', 'FRACTION', 'FREE', 'FUNCTION', 'GETARG', 'GETCHARQQ', 'GETCL', 'GETDAT', 'GETENV', 'GETTIM', 'GO', 'GOTO', 'HFIX', 'HUGE', 'IABS', 'IACHAR', 'IAND', 'IBCHNG', 'IBCLR', 'IBITS', 'IBSET', 'ICHAR', 'ID', 'IDATE', 'IDENTIFIER', 'IDIM', 'IDINT', 'IDNINT', 'IEOR', 'IF', 'IFIX', 'IIABS', 'IIAND', 'IIBCLR', 'IIBITS', 'IIBSET', 'IIDIM', 'IIDINT', 'IIDNNT', 'IIEOR', 'IIFIX', 'IINT', 'IIOR', 'IIQINT', 'IIQNNT', 'IISHFT', 'IISHFTC', 'IISIGN', 'ILEN', 'IMAG', 'IMAX0', 'IMAX1', 'IMIN0', 'IMIN1', 'IMOD', 'IMPLICIT', 'IN', 'INCLUDE', 'INDEX', 'ININT', 'INOT', 'INOUT', 'INQUIRE', 'INT', 'INT1', 'INT1', 'INT2', 'INT2', 'INT4', 'INT4', 'INT8', 'INTC', 'INTEGER', 'INTENT', 'INTERFACE', 'INTRINSIC', 'INTRUP', 'INVALOP', 'IOLENGTH', 'IOMSG', 'IOR', 'IOSTAT', 'IOSTAT_MSG', 'IQINT', 'IQNINT', 'ISHA', 'ISHC', 'ISHFT', 'ISHFTC', 'ISHL', 'ISIGN', 'ISNAN', 'IZEXT', 'JFIX', 'JIAND', 'JIBCLR', 'JIBITS', 'JIBSET', 'JIDIM', 'JIDINT', 'JIDNNT', 'JIEOR', 'JIFIX', 'JINT', 'JIOR', 'JIQINT', 'JIQNNT', 'JISHFT', 'JISHFTC', 'JISIGN', 'JMAX0', 'JMAX1', 'JMIN0', 'JMIN1', 'JMOD', 'JNINT', 'JNOT', 'JZEXT', 'KIABS', 'KIAND', 'KIBCLR', 'KIBITS', 'KIBSET', 'KIDIM', 'KIDINT', 'KIDNNT', 'KIEOR', 'KIFIX', 'KIND', 'KIND', 'KINT', 'KIOR', 'KISHFT', 'KISHFTC', 'KISIGN', 'KMAX0', 'KMAX1', 'KMIN0', 'KMIN1', 'KMOD', 'KNINT', 'KNOT', 'KZEXT', 'LACFAR', 'LBOUND', 'LEADZ', 'LEN', 'LEN', 'LEN_TRIM', 'LENLGE', 'LGE', 'LGT', 'LLE', 'LLT', 'LOCKING', 'LOCNEAR', 'LOG', 'LOG10', 'LOGICAL', 'LOGICAL', 'LSHIFT', 'MALLOC', 'MAP', 'MATMUL', 'MAX', 'MAX0', 'MAX1', 'MAXEXPONENT', 'MAXLOC', 'MAXVAL', 'MERGE', 'MIN', 'MIN0', 'MIN1', 'MINEXPONENT', 'MINLOC', 'MINVAL', 'MOD', 'MODULE', 'MODULO', 'MVBITS', 'NAME', 'NAMED', 'NAMELIST', 'NARGS', 'NBREAK', 'NDPERR', 'NDPEXC', 'NEAREST', 'NEXTREC', 'NINT', 'NML', 'NONE', 'NOT', 'NULLIFY', 'NUMBER', 'NUMBER_OF_PROCESSORS', 'NWORKERS', 'OFFSET', 'ONLY', 'OPEN', 'OPENED', 'OPERATOR', 'OPTIONAL', 'OUT', 'OVEFL', 'PACK', 'PAD', 'PARAMETER', 'PASS', 'PAUSE', 'PEEKCHARQQ', 'PENDING', 'POINTER', 'POPCNT', 'POPPAR', 'POS', 'POSITION', 'PRECFILL', 'PRECISION', 'PRECISION', 'PRESENT', 'PRINT', 'PRIVATE', 'PROCEDURE', 'PRODUCT', 'PROGRAM', 'PROMPT', 'PROTECTED', 'PUBLIC', 'QABS', 'QACOS', 'QACOSD', 'QASIN', 'QASIND', 'QATAN', 'QATAN2', 'QATAND', 'QCMPLX', 'QCONJG', 'QCOS', 'QCOSD', 'QCOSH', 'QDIM', 'QEXP', 'QEXT', 'QEXTD', 'QFLOAT', 'QIMAG', 'QLOG', 'QLOG10', 'QMAX1', 'QMIN1', 'QMOD', 'QREAL', 'QSIGN', 'QSIN', 'QSIND', 'QSINH', 'QSQRT', 'QTAN', 'QTAND', 'QTANH', 'QUOTE', 'RADIX', 'RAN', 'RAND', 'RANDOM', 'RANDOM_NUMBER', 'RANDOM_SEED', 'RANDU', 'RANGE', 'READ', 'READWRITE', 'REAL', 'REAL', 'REC', 'RECL', 'RECURSIVE', 'REPEAT', 'RESHAPE', 'RESULT', 'RETURN', 'RETURN1', 'REWIND', 'REWRITE', 'RRSPACING', 'RSHIFT', 'SAVE', 'SCALE', 'SCAN', 'SECNDS', 'SEGMENT', 'SELECT', 'SELECTCASE', 'SELECTED_INT_KIND', 'SELECTED_REAL_KIND', 'SELECTTYPE', 'SEQUENTIAL', 'SET_EXPONENT', 'SETDAT', 'SETTIM', 'SEQUENCE', 'SHAPE', 'SIGN', 'SIGN', 'SIN', 'SIND', 'SINH', 'SIZE', 'SIZE', 'SIZEOF', 'SNGL', 'SNGLQ', 'SPACING', 'SPREAD', 'SQRT', 'STAT', 'STATUS', 'STOP', 'STREAM', 'SUBMODULE', 'SUBROUTINE', 'SUM', 'SYSTEM', 'SYSTEM_CLOCK', 'TAN', 'TAND', 'TANH', 'TARGET', 'THEN', 'TIMER', 'TINY', 'TO', 'TRANSFER', 'TRANSPOSE', 'TRIM', 'TYPE', 'UBOUND', 'UNDFL', 'UNFORMATTED', 'UNION', 'UNIT', 'UNLOCK', 'UNPACK', 'USE', 'VAL', 'VALUE', 'VERIFY', 'VIRTUAL', 'VOLATILE', 'VOLATILE', 'WAIT', 'WHERE', 'WHILE', 'WRITE', 'ZABS', 'ZCOS', 'ZEXP', 'ZLOG', 'ZSIN', 'ZSQRT']
    ##compiler directives, not used
    reservedCD = ['ALIAS', 'ASSUME_ALIGNED', 'ATTRIBUTES', 'DECLARE', 'DEFINE', 'DISTRIBUTE POINT', 'ELSE', 'ELSEIF', 'ENDIF', \
        'FIXEDFORMLINESIZE', 'FREEFORM', 'IDENT', 'IF', 'IF DEFINED', 'INTEGER', 'IVDEP', 'LOOP COUNT', 'MEMREF_CONTROL', 'MESSAGE', 'NODECLARE' \
        'NOFREEFORM', 'NOPARALLEL', 'NOOPTIMIZE', 'NOPREFETCH', 'NOSTRICT', 'NOSWP', 'NOUNROLL', 'NOVECTOR', 'OBJCOMMENT', 'OPTIMIZE', 'OPTIONS', \
        'PACK', 'PARALLEL', 'PREFETCH', 'PSECT', 'REAL', 'STRICT', 'SWP' , 'UNDEFINE', 'UNROLL', 'VECTOR ALIGNED', 'VECTOR ALWAYS', 'VECTOR NONTEMPORAL', \
        'VECTOR UNALIGNED']
    reservedOPSpecifiers = ['.FALSE.', '.TRUE.', 'ACCESS', 'ACTION', 'APOSTROPHE', 'APPEND', 'ASIS', 'ASSOCIATEVARIABLE', 'ASYNCHRONOUS', \
        'BIG_ENDIAN', 'BINARY', 'BLOCKSIZE', 'BUFFERCOUNT', 'BUFFERED', 'CARRIAGECONTROL', 'COMMA', 'COMPATIBLE', 'CONVERT', 'CRAY', 'DECIMAL', \
        'DEFAULT', 'DEFAULTFILE', 'DELETE', 'DELIM', 'DENTNONE', 'DENYRD', 'DENYRW', 'DENYWR', 'DIRECT', 'DOWN', 'ENCODING', 'ERR', 'FDX', 'FGX', \
        'FILE', 'FIXED', 'FORM', 'FORMATTED', 'FORTRAN', 'IBM', 'IOFOCUS', 'IOSTAT', 'ISTAT', 'KEEP', 'LIST', 'LITTLE_ENDIAN', 'MAXREC', 'NAME', \
        'NATIVE', 'NEAREST', 'NEW', 'NEWUNIT', 'NO', 'NONE', 'NOSHARED', 'NULL', 'OLD', 'ORGANIZATION', 'PAD', 'PLUS', 'POINT', 'POSITION', 'PRINT', \
        'PRINT/DELETE', 'PROCESSOR_DEFINED', 'QUOTE', 'READ', 'READONLY', 'READWRITE', 'RECL', 'RECORDSIZE', 'RECORDTYPE', 'RELATIVE', 'REPLACE', \
        'REWIND', 'ROUND', 'SCRATCH', 'SEGMENTED', 'SEQUENTIAL', 'SHARE', 'SHARED', 'SIGN', 'STATUS', 'STREAM', 'STREAM_CR', 'STREAM_LF', 'SUBMIT', \
        'SUBMIT/DELETE', 'SUPPRESS', 'TITLE', 'TYPE', 'UNFORMATTED', 'UNIT', 'UNKNOWN', 'UP', 'USEROPEN', 'UTF-8', 'VARIABLE', 'VAXD', 'VAXG', \
        'WRITE', 'YES', 'ZERO']
    ## dont need this library
    # reservedLibraries = ['DFWIN', 'DFLIB', 'DFPORT', 'SIMEOBJ']
    ## .F file use INTEGER X1,X2,X3,
    ##             & X4,X5,X6
    ## .FOR files use INTEGER X1,X2,X3,
    ##                $X4,X5,X6
    reservedIdentifier = ['INTRINSIC','COMMON','EQUIVALENCE', 'COMPLEX', 'DATA', 'LOGICAL', 'INTEGER', 'DOUBLE', 'PRECISION', 'REAL', 'CHARACTER', \
        'EXTERNAL', 'TYPE', 'DIMENSION', 'SAVE', 'RECORD', 'STRUCTURE']
    reservedVarOption = ['PARAMETER', 'ALLOCATABLE', 'SAVE' ]
    reservedSpecialCase = ['CHANGE', 'THE', 'EXC', 'iparmtype', 'parmnam']

    symbolList = ['=', '+', '-', '*','/', ',']
    newLine = ''
    ##create new list by replacing all symbols with commas
    ## work with comments   TODO LIST
    ### TODO: 5/13 - THE DECLARE FUNCTION REMOVED ALL THE INCLUDE VARIABLES
    for i in range(len(lines2)):
        ## CAN PLACE LINES2[I].UPPER() HERE TO IMPROVE EFFICIENCY
        # newLine = lines2[i][:-1] ##<---# TODO:  ignore the \n character, I will have to change all the \n and newLine[0] variables
        if len(lines2[i]) > 73:
            newLine = lines2[i][:73]
        else:
            newLine = lines2[i]
        ##TODO REWORK THIS TO ASSOCIATE WITH DEFINE/ IF / DECLARE
        ## ignore comment block
        #ignores any comments from the newLine
        ##      ex. !DEC$ IF DEFINED (PRECARNBUILD)
        ##      ex. CD      OLD CODE
        if re.search("^[cCdD!*]", newLine[0]) or lines2[i] == '\n':
            continue

        ## clears comments after the code
        ##      ex. NLFBUS = L !---COMMENTCOMMENTCOMMENT---
        if '!' in newLine:
            newLine = newLine[:newLine.find('!')]

        ## continued single quote line removed
        if len(newLine) > 6 and not ' ' in newLine[5] and hasQuote:
            RightIndex6 = newLine.find('\'')
            newLine = '     ' + newLine[RightIndex6+1:]
        countQuote = 0
        LeftIndex6 = 0
        RightIndex6 = 0
        hasQuote = False
        totalQuote = newLine.count('\'') /2
        ## if FORMAT not in newLine.upper or not isFormat:
        ## IGNORE FORMAT FUNCTION LINE

        if ' INCLUDE ' not in newLine.upper() and (newLine.find('\'') != -1) :
            while(countQuote < totalQuote):
                LeftIndex6 = newLine.find('\'')
                RightIndex6 = newLine.find('\'', LeftIndex6+1)
                newLine = newLine[:LeftIndex6] +  newLine[RightIndex6+1:]
                if RightIndex6 == -1: ## no more quotations
                    hasQuote = True
                    newLine = newLine[:LeftIndex6]
                countQuote = countQuote + 1
        ## removing double quotations
        if len(newLine) > 6 and not ' ' in newLine[5] and hasDblQuote:
            RightIndex7 = newLine.find('\"')
            newLine = newLine[RightIndex7+1:]

        countDblQuote = 0
        LeftIndex7 = 0
        RightIndex7 = 0
        hasDblQuote = False
        totalDblQuote = newLine.count('\"') /2

        ## if FORMAT not in newLine.upper or not isFormat:
        ## IGNORE FORMAT FUNCTION LINE
        if ("INCLUDE" not in newLine.upper()) and (newLine.find('\"') != -1) :
            while(countDblQuote < totalDblQuote):
                LeftIndex7 = newLine.find('\"')
                RightIndex7 = newLine.find('\"', LeftIndex7+1)
                newLine = newLine[:LeftIndex7] + newLine[RightIndex7+1:]
                if RightIndex7 == -1: ## no more quotations
                    hasDblQuote = True
                    newLine = newLine[:LeftIndex7]
                countDblQuote = countDblQuote + 1

        ##ignore line block
        ##subroutine, function block
        if 'SUBROUTINE' in newLine.upper():
            # varList = []
            # exList = [] ## not neccessary to clear the .f90 file
            hasImplicit = False
            if newLine.endswith(',\n'):
                isSubroutine = True
            continue
        # add function into varList
        elif 'FUNCTION' in newLine.upper():
            functionIndex1 = newLine.upper().find('FUNCTION ')
            functionIndex2 = newLine.upper().find('(')
            hasImplicit = False
            varList.append(newLine[functionIndex1+9:functionIndex2].strip().upper())
            if newLine.endswith(',\n'):
                isFunction = True
            continue
        ## put the entry function name into the variable list
        elif re.search(r'\b'+'ENTRY '+r'\b', newLine.upper()):        #'ENTRY ' in newLine.upper():
            functionIndex1 = newLine.find('ENTRY ')
            varList.append(newLine[functionIndex1+6:])
            continue
        elif isSubroutine or isFunction:
            if newLine.endswith(')\n'):
                isSubroutine = False
                isFunction = False
            continue
        elif 'IMPLICIT NONE' in newLine.upper():
            hasImplicit = True
            prevVar = []
        elif USE_REGEX.match(newLine):
            tempMatch = USE_REGEX.match(newLine)
            extendedVarList = addLibraryFiles(tempMatch.group(2), fileLocation)
            # extendedVarList = addLibraryFiles(newLine[newLine.find(' ')+1:], fileLocation)
            for ii in extendedVarList[1]:
                exList.append(ii)
            continue
        elif INCLUDE_REGEX.match(newLine):
            tempMatch = INCLUDE_REGEX.match(newLine)
            if '.INC' in tempMatch.group(1).upper():
                os.chmod(fileLocation+tempMatch.group(1), 0o444)
                lines10 = [line10 for line10 in open(fileLocation+tempMatch.group(1))]
                for i in range(len(lines10)):
                    if INCLUDE_REGEX.match(lines10[i]):
                        tempMatch = INCLUDE_REGEX.match(lines10[i])
                        extendedVarList = INCLUDE_addLibraryVariables(tempMatch.group(1), fileLocation)
                        for ii in extendedVarList:
                            exList.append(ii)
            else:
                extendedVarList = INCLUDE_addLibraryVariables(tempMatch.group(1), fileLocation)
                for ii in extendedVarList:
                    exList.append(ii)
        elif newLine.upper().startswith('      RETURN'):
            continue
        ##variables such as i,j,...n are implited as integers, the rest are real
        if not hasImplicit:
            continue
        ## variable block
        ## remove the excess details from CHARACTER*1 SARRAY(800)
        ## ignore COMMON, DIMENSION and EQUIVALENCE
        # this is for extended variable declarations
        #       INTEGER Y1, Y2, Y3,
        #      & Y4, Y5, Y6
        ## any character can be used as a continuation line in newLine[5], conventionally *,+,&,\, are used, but 0-9a-zA-Z can also be used
        if len(newLine) > 6 and not ' ' in newLine[5] and (hasIdentifier or ext_hasIdentifier):
            ext_hasIdentifier = True
            # print ("H: " + str(hasIdentifier) + " exH: " + str(ext_hasIdentifier))
            # print (newLine)
        else:
            ext_hasIdentifier = False
        hasIdentifier = False
        for ii in range(len(reservedIdentifier)):
            if re.search(r'\b' + reservedIdentifier[ii] + r'\b', newLine.upper()):
                hasIdentifier = True
                newLine = newLine.strip()
                newLine = newLine[len(reservedIdentifier[ii])-0:]


        # print ("H: " + str(hasIdentifier) + " exH: " + str(ext_hasIdentifier))
        # print (newLine)
        # print (ext_hasIdentifier)

        ## begin removing excess symbols
        ##      ex CHARACTER*128 CH2, CNM(YU)
        ##          DIMENSION TS1(NP*4)
        ##          DIMENSION :: TSOP
        if hasIdentifier and '::' in newLine:
            newLine = newLine[newLine.find('::')+2:]

        ##remove FORMAT FUNCTION
        if "FORMAT" in newLine.upper(): ## or re.search(r'\b'+ 'WRITE[ ]*\(', newLine.upper()):
            isFormat = True
            continue
        elif isFormat and len(newLine) > 5 and \
            not ' ' in newLine[5]:
                continue
        else:
            isFormat = False
        ##removes all logic expressions from line
        newLine = LOGIC_REGEX.sub(' ', newLine)

    ##function name strip block
        #strips the leading brackets, dont need the function name
        #VALIN(1)=SQRT(PDG(JY+1)*PDG(JY+1)+PQG(JY+1)*PQG(JY+1))
        #WS1=10*GENPQ(SMG)
        # WS1=GENPQ(1,JJ)*GMW(IWS3-1)/100.0
        # WS1=(1,JJ)*(IWS3-1)/100.0<----- new
        # ALLOCATE(JREBUS_TMP(1:NLFBUS),STAT=JJ)
        # (JREBUS_TMP((1:NLFBUS),STAT=JJ)<----- new
        # flags: GENPQ, IDISPFLAG, IWS1=MNEW, MNEW(JJ), ASTOP
        if not (hasIdentifier or ext_hasIdentifier):
            newLine1 = newLine
            rBracket = newLine.rfind('(')
            cIndex = len(newLine) -1
            innerSymbol = False
            if rBracket != -1:
                for j in range(len(newLine)-1, -1 , -1):
                    if newLine[j] ==')' and cIndex == len(newLine) -1:
                        newLine1 = newLine[j+1:]
                        cIndex = j
                        innerSymbol = True
                    elif newLine[j] == ')' and innerSymbol:
                        if not newLine[cIndex] == '(':
                            newLine1 = newLine[j:cIndex+1] + newLine1
                        cIndex = j
                    elif newLine[j] ==')' and not innerSymbol:
                        if not newLine[cIndex] == '(':
                            newLine1 = newLine[j:cIndex+1] + newLine1
                        cIndex = j
                        innerSymbol = True
                    elif newLine[j] == '(' and cIndex == len(newLine) -1:
                        newLine1 = newLine[j:]
                        cIndex = j
                        innerSymbol = False
                    elif newLine[j] == '(' and innerSymbol:
                        ## for nested statements
                        if newLine1[0] == ')':
                            newLine1 = newLine[j:cIndex+0] + newLine1
                        else:
                            newLine1 = newLine[j:cIndex+1] + newLine1
                        cIndex = j
                        innerSymbol = False
                    elif newLine[j] == '(' and not innerSymbol:
                        if newLine[cIndex] == '(':
                            newLine1 = newLine[j:j+1] + newLine1
                        cIndex = j
                    elif  newLine[cIndex] in symbolList and j == 0:
                        newLine1 = newLine[0:cIndex+1] + newLine1
                    elif newLine[j] in symbolList and not innerSymbol:
                        if newLine[cIndex] == '(':
                            cIndex = j
            newLine = newLine1
        # print("Time taken by functions: " + str(time.time()- initTime) +"s function skip block" + fileName)
        ## strips brackets that expands over multiple lines\
        ## FIXED WITH ABOVE LOOP
        ##issues:
        ## fixed with the above function
        ##                TY = RTY + RUY(SP, RP, QP,QR(YU,UI),
        ##                CALL ASTOP(' *** ERROR - ALLOCATING VICINITY' //
        ##                READ AVC(SOM,THI,NG,
        # if newLine.count('(') == 1 and newLine.count(')') == 0 and (newLine.endswith(',') or newLine.endswith('//')):
        #     newLine = newLine[:newLine.rfind(' ')+1] + newLine[newLine.find('(')+1:]

        newLine = re.sub('[^a-zA-Z0-9\n\.\_]', ',', newLine.strip())
        if newLine.startswith(',') or newLine.endswith(','):
            newLine = re.sub(',+', ',', newLine).strip(',')
        else:
            newLine = re.sub(',+', ',', newLine)
        newList = newLine.split(',')

        ##removes the CALL function names
        if ('CALL' in newList or 'call' in newList) and \
            len(newList) == 1:
            continue
        elif 'CALL' in newList:
            newList.pop(newList.index('CALL')+1)
        elif 'call' in newList:
            newList.pop(newList.index('call')+1)
        # if len(newList) == 2 and newList[0].upper() == 'CALL':
        #     continue
    ##CHECKS IF VARIABLE WAS PREVIOUSLY DECLARED, MAIN FUNCTION OF ERROR6404
        # print("Time taken by functions: " + str(time.time()- initTime) +"s prevariable check block")

        if newList:
            for ii in newList:
                if (hasIdentifier or ext_hasIdentifier) and \
                    ii.upper() not in varList and \
                    ii.isidentifier():
                        varList.append(ii.upper())
                if not ii.upper() in reservedList and \
                    not ii.upper() in reservedIdentifier and \
                    not ii.upper() in reservedNotepadKey and \
                    not ii.upper() in reservedVarOption and \
                    not ii.upper() in reservedSpecialCase and \
                    not ii.upper() in reservedOPSpecifiers and \
                    not ii.upper() in prevVar and \
                    not ii.upper() in varList and \
                    not ii.upper() in exList and \
                    ii.isidentifier():
                        prevVar.append(ii.upper())
                        F.write(newFileName + '(' + str(i+1) + ') error #6404: ['+ ii + '] \n')
                        F.flush()

    # print("Time taken by functions: " + str(time.time()- initTime) +"s post variable check block")
    print("[Complete]")
    F.close()

##adds variables from library to the list, used by error findError6404
def INCLUDE_addLibraryVariables(fileName, fileLocation):
    newFileName = fileName
    tempVarList = []
    ## strip the excess from use library
    # ex. flopsf_data,,IBTYPE_DUMMY,,,,IBTYPE.f90
    #---------^       Only want this element
    if ',' in fileName:
        newFileName = fileName[:fileName.find(',')] + ".f90"
    reservedIdentifier = ['COMMON', 'EQUIVALENCE', 'COMPLEX', 'LOGICAL', 'INTEGER', 'REAL', 'CHARACTER', 'EXTERNAL' , '+', '&', 'INCLUDE' \
                        'TYPE', 'DIMENSION', 'PARAMETER', 'ALLOCATABLE']
    reservedList = ['MODULE', 'SUBROUTINE', 'END', 'FUNCTION', 'INTERFACE', 'IMPLICIT', 'NONE', 'SAVE', 'TYPE']
    fName = fileLocation + newFileName
    os.chmod(fName, 0o444)
    lines8 = [line8 for line8 in open(fName)]

    for i in range(len(lines8)):
        newLine = lines8[i]
        ## for f90 variables
        if '::' in newLine:
            newLine = newLine[newLine.find('::'):]
        newLine = re.sub('[^a-zA-Z0-9\n\.\_]', ',', newLine.strip())
        # print (newLine)
        while(newLine.startswith(',')):
            newLine = newLine[1:]
        while(newLine.endswith(',')):
            newLine = newLine[0:len(newLine)-1]

        LeftIndex4 = 0
        RightIndex4 = 0
        while(LeftIndex4 != -1):
            if "C" in lines8[i][0] or "*" in lines8[i][0] or "!" in lines8[i][0] or newLine =='':
                    break
            if(LeftIndex4 == RightIndex4):
                RightIndex4 = newLine.find(',')
            elif (LeftIndex4 != -1 and RightIndex4 == -1):
                RightIndex4 = len(newLine)
            else:
                if LeftIndex4 == 0:
                    if not newLine[LeftIndex4:RightIndex4].upper() in reservedIdentifier and \
                        not newLine[LeftIndex4:RightIndex4].upper() in reservedList and \
                        not newLine[LeftIndex4:RightIndex4].upper() in tempVarList and \
                        newLine[LeftIndex4:RightIndex4].isidentifier():
                            tempVarList.append(newLine[LeftIndex4:RightIndex4].upper())
                            # print (newLine[LeftIndex4:RightIndex4].upper() + "!!1")
                    LeftIndex4 = newLine.find(',')
                    RightIndex4 = newLine.find(',', LeftIndex4 + 1)
                else:
                    if not newLine[LeftIndex4+1:RightIndex4].upper() in reservedIdentifier and \
                        not newLine[LeftIndex4+1:RightIndex4].upper() in reservedList and \
                        not newLine[LeftIndex4+1:RightIndex4].upper() in tempVarList and \
                        newLine[LeftIndex4+1:RightIndex4].upper().isidentifier():
                            tempVarList.append(newLine[LeftIndex4+1:RightIndex4].upper())
                            # print (newLine[LeftIndex4+1:RightIndex4].upper() + "!!2")
                    LeftIndex4 = newLine.find(',', LeftIndex4 + 1)
                    RightIndex4 = newLine.find(',', LeftIndex4 + 1)
    return tempVarList
##adds variables for F90 extention files
## might change to ordered tuple
def addLibraryVariables(fileName, fileLocation, fileList=[], varList=[]):
    reservedIdentifier = ['COMMON', 'EQUIVALENCE', 'COMPLEX', 'LOGICAL', 'INTEGER', 'REAL', 'CHARACTER', 'EXTERNAL' , '+', '&', 'INCLUDE' \
                        'TYPE', 'DIMENSION', 'PARAMETER', 'ALLOCATABLE']
    reservedList = ['MODULE', 'SUBROUTINE', 'END', 'FUNCTION', 'INTERFACE', 'IMPLICIT', 'NONE', 'SAVE', 'TYPE']
    tempFileList = []
    tempVarList = []
    hasLibrary = False
    newFileName = fileName.upper()

    ## strip the excess from use library
    # ex. flopsf_data, ONLY: VAR1
    #---------^       Only want this element
    if ',' in fileName:
        newFileName = fileName[:fileName.find(',')]
    ##EXIT 0
    if newFileName in fileList:
        return fileList, varList
    # if '.INS' not in newFileName:
    for fileF90 in glob.iglob(fileLocation + "*.f90"):
        ##check if .F90 file is in the directory
        if re.search (r'\b' + newFileName + r'\b', fileF90.upper()):
            # return fileList, varList
            hasLibrary = True
    if not hasLibrary:
        return fileList, varList

    fileList.append(newFileName)

    fName =  fileLocation + newFileName + ".f90"
    # fName =  fileLocation + newFileName
    # if not '.INS' in fName:
    #     fName = fName + ".f90"
    os.chmod(fName, 0o444)
    lines8 = [line8 for line8 in open(fName)]

    for i in range(len(lines8)):
        newLine = lines8[i].upper()
        ##EXIT 1
        if newLine.upper().startswith("USE "):
            tempName = newLine.strip()
            tempName = tempName[tempName.find(' ')+1:]
            tempFileList, tempVarList = addLibraryVariables(tempName, fileLocation, fileList, varList)

        if '!' in newLine:
            newLine = newLine[:newLine.find('!')]
        if 'MODULE ' in newLine or 'SUBROUTINE ' in newLine:
            continue

        if '%' in newLine:
            newLine = newLine[newLine.rfind('%')+1:]
        if '::' in newLine:
            newLine = newLine[newLine.find('::')+2:]
            if '=' in newLine:
                newLine = newLine[:newLine.rfind('=')]


        newLine = re.sub('[^a-zA-Z0-9\n\.\_]', ',', newLine.strip())
        # print (newLine)
        while(newLine.startswith(',')):
            newLine = newLine[1:]
        while(newLine.endswith(',')):
            newLine = newLine[0:len(newLine)-1]

        LeftIndex4 = 0
        RightIndex4 = 0
        while(LeftIndex4 != -1):
            if "C" in lines8[i][0] or "*" in lines8[i][0] or "!" in lines8[i][0] or newLine =='':
                    break
            if(LeftIndex4 == RightIndex4):
                RightIndex4 = newLine.find(',')
            elif (LeftIndex4 != -1 and RightIndex4 == -1):
                RightIndex4 = len(newLine)
            else:
                if LeftIndex4 == 0:
                    if not newLine[LeftIndex4:RightIndex4].upper() in reservedIdentifier and \
                        not newLine[LeftIndex4:RightIndex4].upper() in reservedList and \
                        not newLine[LeftIndex4:RightIndex4].upper() in varList and \
                        not newLine[LeftIndex4:RightIndex4].upper() in tempVarList and \
                        newLine[LeftIndex4:RightIndex4].isidentifier():
                            varList.append(newLine[LeftIndex4:RightIndex4].upper())
                    LeftIndex4 = newLine.find(',')
                    RightIndex4 = newLine.find(',', LeftIndex4 + 1)
                else:
                    if not newLine[LeftIndex4+1:RightIndex4].upper() in reservedIdentifier and \
                        not newLine[LeftIndex4+1:RightIndex4].upper() in reservedList and \
                        not newLine[LeftIndex4:RightIndex4].upper() in varList and \
                        not newLine[LeftIndex4+1:RightIndex4].upper() in tempVarList and \
                        newLine[LeftIndex4+1:RightIndex4].upper().isidentifier():
                            varList.append(newLine[LeftIndex4+1:RightIndex4].upper())
                    LeftIndex4 = newLine.find(',', LeftIndex4 + 1)
                    RightIndex4 = newLine.find(',', LeftIndex4 + 1)
    return fileList, varList
##adds variables for F90 extensions
def addLibraryFiles(fileName, fileLocation):
    modFileName = ''
    modFile = ''
    for file in glob.glob(fileLocation+ '**/*.mod', recursive=True):
        if fileName.upper() in file.upper():
            modFile = file
    if modFile:
        os.chmod(modFile, 0o444)
        lines8 = [line8 for line8 in open(modFile, errors='ignore')]
        for i in range(len(lines8)):
            if '.F90' in lines8[i].upper():
                modFileName = lines8[i][lines8[i].rfind('\\')+1:lines8[i].rfind('.f90')]
    if not modFileName:
        modFileName = fileName
    return addLibraryVariables(modFileName, fileLocation)
