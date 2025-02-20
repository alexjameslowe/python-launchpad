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

SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))


def getVarURI(varName):
  createVarsIfNeeded()
  uri = joinPath(SCRIPT_DIR, 'vars', f'--{varName}.txt')
  return uri

def getVarsDirPath():
  return joinPath(SCRIPT_DIR, 'vars')

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