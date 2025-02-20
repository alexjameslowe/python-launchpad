import argparse, sys
import os
from os import path
import sys
from time import sleep

# import warnings
# warnings.simplefilter(action = "ignore", category = RuntimeWarning)


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, rmVar, getVar, RUNNING, PROCESS, GRACEFUL_EXIT


def startTask():
  
  #Set this to false to start with
  setVar(GRACEFUL_EXIT, False)

  #Set this to True
  setVar(RUNNING, True)


def gracefulExit(msg=""):  
  if(getVar(GRACEFUL_EXIT, asbool=True)):
    raise Exception(f"Graceful exiting {msg}")
  

def endTask():
  
  #We got to the end, so set running to false
  #and remove the process id.
  setVar(RUNNING, False)
  rmVar(PROCESS)
