####################################################################################
#
#  A non-thread disk variable utility to be used outside the virtual-environment
#  specifically to help the VEnv utility keep track of the idempotence for 
#  performing pip install when the requirements change
# 
####################################################################################


import sys 
from os import path, mkdir
from python_launchpad.utils.Format import joinPath
from python_launchpad.utils.Configure import getDataDirectory
from python_launchpad.utils.File import removeIfExists

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

MODE_NORMAL = 'normal'
MODE_THREADSAFE = 'cleanup'
MODE = MODE_NORMAL

def setVarsToNormal():
  global MODE 
  MODE = MODE_NORMAL

def setVarsToThreadSafe():
  global MODE 
  MODE = MODE_THREADSAFE

def getVarURI(varName):
  createVarsIfNeeded()
  pfx = '--' if MODE == MODE_NORMAL else '__'
  uri = joinPath(getVarsDirPath(), f'{pfx}{varName}.txt')
  return uri

##
# get the directory of the variables
#
def getVarsDirPath():
  return joinPath(getDataDirectory(), 'vars')


def createVarsIfNeeded():
  varsDirPath = getVarsDirPath()
  if(not path.isdir(varsDirPath)):
    mkdir(varsDirPath)
    
def setVar(varName, value="empty"):
  createVarsIfNeeded()
  
  #Make the file and add in the text
  with open(getVarURI(varName), "w+") as f:
    if(not value):
      f.write("None")
    else:
      f.write(str(value))


def getVar(varName, defval=None):
  createVarsIfNeeded()
  
  varContents = None

  if(not isVar(varName)):
    return defval

  with open(getVarURI(varName), 'r') as f:
    varContents = f.read()

  return varContents

def isVar(varName):
  createVarsIfNeeded()
  doesExist = path.isfile(getVarURI(varName))
  return doesExist

def rmVar(varName):
  createVarsIfNeeded()
  removeIfExists(getVarURI(varName))
