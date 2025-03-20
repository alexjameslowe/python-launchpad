##########################################################################################
#
#  An example background long-running task. Note the use of startTask(), gracefulExit()
#  and endTask(). 
# 
#  It's important to observe the structure of this file.
#  There must be a try-except-finally block. endTask() must always be called in finally 
#  so that it will fire even if there's an error. gracefulExit() will raise an exception
#  in the event that the user has gracefully exited.
#  
#  Author Alex Lowe
#
##########################################################################################

from os import path
from sys import path as syspath
from time import sleep

# import warnings
# warnings.simplefilter(action = "ignore", category = RuntimeWarning)

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))

from python_launchpad.utils.TaskRunner import startTask, gracefulExit, endTask
  
#Run the report on a background processes, and gather information about what's going
#on to the user to update the screen as we go.
def task(args):
  
  startTask()

  try:

    sleep(2)
    print(f"Do the hard time-consuming thing here. 0. Here's the show_this: {str(args.get('show_this', 0))}")

    gracefulExit("Exiting here 549382")
   
    sleep(2)
    print("Do the hard time-consuming thing here. 1")
    sleep(2)
    print("Do the hard time-consuming thing here. 2")
    sleep(2)
    print("Do the hard time-consuming thing here. 3")
    sleep(2)
    print("Do the hard time-consuming thing here. 4")
    sleep(2)


    gracefulExit("Exiting here 119384")

    print("Do the hard time-consuming thing here. 5")
    sleep(2)
    print("Do the hard time-consuming thing here. 6")
    sleep(2)
    print("Do the hard time-consuming thing here. 7")
    sleep(2)
    print("Do the hard time-consuming thing here. 8")
    sleep(2)


  except Exception as err:
    print(f"Error caught in report: {str(err)}")


  finally:

    endTask()

