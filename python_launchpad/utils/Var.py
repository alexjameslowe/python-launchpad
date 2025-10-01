import sys
import os
from os import path
import sys
#import fcntl #for linux
import json
import portalocker  #for windows
from python_launchpad.utils.Configure import getDataDirectory
from python_launchpad.utils.Format import joinPath

#############################################################
#
# Handy functions for cross-process communication
#
#############################################################


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))


FILE_ERRS = 'FILE_ERRS'
UNKNOWN_ERRS = 'UNKNOWN_ERRS'
DAYS_REPORTED = 'DAYS_REPORTED'
DAYS_SKIPPED = 'DAYS_SKIPPED'
PROCESS = 'PROCESS'
GRACEFUL_EXIT = 'GRACEFUL_EXIT'
RUNNING = 'RUNNING'
FILES_WRITTEN = 'FILES_WRITTEN'
DIRS_CREATED = 'DIRS_CREATED'
ERROR = 'ERROR'
WARNING = 'WARNING'


# For linux. a pity we still have these xplatform problems
# #https://stackoverflow.com/questions/4843359/python-lock-a-file
# def acquireLock(varName):
#     ''' acquire exclusive lock file access '''
#     locked_file_descriptor = open(getVarLockURI(varName), 'w+')
#     fcntl.lockf(locked_file_descriptor, fcntl.LOCK_EX)
#     return locked_file_descriptor

# def releaseLock(locked_file_descriptor):
#     ''' release exclusive lock file access '''
#     locked_file_descriptor.close()

def removeIfExists(uriPath):
  if path.exists(uriPath):
    os.remove(uriPath)

##
# get the directory of the variables
#
def getVarsDirPath():
  return joinPath(getDataDirectory(), 'vars')


##
# create the var directory if it doesn't exist
#
def createVarsIfNeeded():
  varsDirPath = getVarsDirPath()
  if(not path.isdir(varsDirPath)):
    os.mkdir(varsDirPath)
    

##
# get the uri to the variable
#
def getVarURI(varName):
  createVarsIfNeeded()
  uri = joinPath(getVarsDirPath(), f'__{varName}.txt')
  return uri


##
# get the uri to the variable lockfile
#
def getVarLockURI(varName):
  createVarsIfNeeded() 
  uri = joinPath(getVarsDirPath(), f'__{varName}_lockfile.LOCK')
  return uri


def isVar(varName):
  createVarsIfNeeded()
  doesExist = path.isfile(getVarURI(varName))
  return doesExist


def appendCSVListVar(varName, stringToAppend):
  createVarsIfNeeded()
  if(not isVar(varName)):
    setVar(varName, stringToAppend)
  else:
    current = getVar(varName)
    newString = f"{current},{stringToAppend}" if current != "None" else stringToAppend
    setVar(varName, newString)


def incVar(varName, increment=1):
  createVarsIfNeeded()
  if(not isVar(varName)):
    setVar(varName, '1')
  else:
    current = getVar(varName, asint=True)
    current += increment
    setVar(varName, current)



def setVar(varName, value="empty", asjson=False):
  createVarsIfNeeded()
  
  #Make the file and add in the text
  with portalocker.Lock(getVarURI(varName), "w+") as f:
    if(not value):
      f.write("None")
    else:
      if(asjson):
        f.write(json.dumps(value))
      else:
        f.write(str(value))


def getVar(varName, defval=None, asjson=False, asint=False, asbool=False, asfloat=False, ascsvlist=False):
  createVarsIfNeeded()
  
  varContents = None

  if(not isVar(varName)):
    return defval

  with portalocker.Lock(getVarURI(varName), 'r') as f:
    varContents = f.read()

  if(varContents == "None"): 
    return defval

  if(asjson):
    return {} if varContents == None or varContents == 'None' else json.loads(varContents)
  elif(asint):
    return 0 if varContents == None or varContents == 'None' else int(varContents)
  elif(asfloat):
    return 0 if varContents == None or varContents == 'None' else float(varContents)
  elif(asbool):
    return str(varContents) == "True"
  elif(ascsvlist):
    varContentsNoNone = '' if varContents == None or varContents == 'None' else varContents
    splitsky = varContentsNoNone.split(',')
    return [] if splitsky == None else splitsky
  else:
    return varContents

def rmVar(varName):
  createVarsIfNeeded()
  removeIfExists(getVarURI(varName))

  


## For Linux
# def isVar(varName):
#   #acquire the lock
#   lock = acquireLock(varName)
#   doesExist = path.isfile(getVarURI(varName))
#   #release the lock
#   releaseLock(lock)
#   return doesExist


# def setVar(varName, value="empty", asjson=False):
  
#   #acquire the lock
#   lock = acquireLock(varName)

#   #Make the file and add in the text
#   with open(getVarURI(varName), "w+") as f:
#     if(not value):
#       f.write("None")
#     else:
#       if(asjson):
#         f.write(json.dumps(value))
#       else:
#         f.write(str(value))

#   #release the lock
#   releaseLock(lock)


# def getVar(varName, asjson=False, asint=False, asbool=False, asfloat=False):
#   varContents = None

#   #acquire the lock
#   lock = acquireLock(varName)

#   with open(getVarURI(varName)) as f:
#     varContents = f.read()

#   #release the lock
#   releaseLock(lock)

  # if(asjson):
  #   return {} if varContents == None else json.loads(varContents)
  # elif(asint):
  #   return 0 if varContents == None else int(varContents)
  # elif(asfloat):
  #   return 0 if varContents == None else float(varContents)
  # elif(asbool):
  #   return str(varContents) == "True"
  # else:
  #   return varContents

# def rmVar(varName):
#   #acquire the lock
#   lock = acquireLock(varName)
#   removeIfExists(getVarURI(varName))
#   #release the lock
#   releaseLock(lock)
  