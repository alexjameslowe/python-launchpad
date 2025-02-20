#########################################################################
#
# Set the GRACEFUL_EXIT variable so that the subprocess 
# knows that it's time to exit.
# 
# Author Alex Lowe
#
########################################################################

import sys
import os

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, GRACEFUL_EXIT

def gracefulExit():
  setVar(GRACEFUL_EXIT, True)
 