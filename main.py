import os
import os.path
from os import path
import glob
# import sys, stat
import re
import pdb
import time
try:
   True
except NameError:
   setattr(__builtins__, 'True', 1)
   setattr(__builtins__, 'False', 0)

def has_key(x, y):
   if hasattr(x, 'has_key'): return x.has_key(y)
   else: return y in x

try:
   import htmlentitydefs
   import urlparse
   import HTMLParser
except ImportError: #Python3
   import html.entities as htmlentitydefs
   import urllib.parse as urlparse
   import html.parser as HTMLParser
try: #Python3
   import urllib.request as urllib
except:
   import urllib
import optparse, re, sys, codecs, types

try: from textwrap import wrap
except: pass

import extract_htm
import Second
import Third
import readErrors
print ("   __               _           _ _   ")
print ("  / _| ___  _ __ __| | __ _  __| | |_ ")
print (" | |_ / _ \| '__/ _` |/ _` |/ _` | __|")
print (" |  _| (_) | | | (_| | (_| | (_| | |_ ")
print (" |_|  \___/|_|  \__,_|\__,_|\__,_|\__|")
print ("converts general error cases for: 6158, 6222, 6239, 6362, 6404, 6401, 6418, 7319 ")
##Fortran files are in a separate folder,
#but can be placed in main folder with fileDir = ""
# fileDir = "tsatv6 - backup\\"
fileDir = ""
fileTxt = "BuildLog.txt"
htmFile = "BuildLog.htm"

time.sleep(2)
if (path.exists(htmFile) == True):
    print ("BuildLog.htm found.")
    print ("Generating build log text file.")
    time.sleep(2)
    extract_htm.buildTxtFile(htmFile)
else:
    print ('No BuildLog.htm found.')
    print ("Generating build log with fordadt.")
    time.sleep(2)
    readErrors.buildTxtFile(fileTxt, fileDir)
time.sleep(2)
fileList = Second.createTextList(fileTxt)
print("\nFixing All Errors\n")
time.sleep(2)
Second.fixAllErrors(fileDir, fileList)
print("\nVariable clean up tool\n")
time.sleep(2)
Third.localFileVariableCleanUp(fileDir)

print ("Files are cleaned ....[END]")
