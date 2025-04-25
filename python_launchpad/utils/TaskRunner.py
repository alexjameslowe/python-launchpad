from os import path
from sys import path as syspath, exc_info
import traceback


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, rmVar, getVar, RUNNING, PROCESS, GRACEFUL_EXIT


# handle the exception
# https://docs.python.org/3/library/http.server.html#http.server.HTTPServer
# 
def handleException():
  exc_type, exc_value, exc_traceback = exc_info()
  lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
  error_string = ''.join(lines)
  print(error_string)
  setVar('ERROR', error_string)


def printMsg():
  pass 
  #TODO: going to have a thing where you print a message, but it also
  #accumulates the messages inside an array, and then the next time the
  #monitor is rendered, it's going to flush them all out to the monitor 
  #and then reset the array.


##
# Call this periodically in your task, and it will gracefully exit your task
#
def gracefulExit(msg=""):  
  if(getVar(GRACEFUL_EXIT, asbool=True)):
    raise Exception(f"Graceful exiting {msg}")
  

##
# start a task. Call this at the start of your try case.
#
def startTask():
  
  #Set this to false to start with
  setVar(GRACEFUL_EXIT, False)

  #Set this to True
  setVar(RUNNING, True)



##
# end a task. This must be called in the finally block of the task.
#
def endTask():
  
  #We got to the end, so set running to false
  #and remove the process id.
  setVar(RUNNING, False)
  rmVar(PROCESS)
  exit()
