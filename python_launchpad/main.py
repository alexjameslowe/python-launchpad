import os
import argparse, sys

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Configure import configure, setProfileSetting, getMainSetting, versionInfo
from python_launchpad.utils.VEnv import activate
from python_launchpad.utils.Task import parseArgs, getTaskInfo
from python_launchpad.utils.Init import init
from python_launchpad.Tasks import TASKS


########################################################################
#
#  Main entrypoint for the program. The main code is fired from with
#  a virtual environment. From within the virtual environment, the 
#  main task is run on a background process, and in the foreground, 
#  the task is monitored with thread-safe variables.
#  
#  author Alex Lowe
#
########################################################################

def main():
    
  parser=argparse.ArgumentParser()
  parser.add_argument('-config', help='Configure the program.', required=False, default=None)
  parser.add_argument('-test', help='Is this a test?', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-set-value', help='Whats the value of the setting youd like to set?', required=False, default=None)
  parser.add_argument('-for-key', help='Which key do you want to set the value for?', required=False, default=None)
  parser.add_argument('-v', help='Get version info', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-graceful-exit', help='Do you want to exit gracefully?', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-background', help='Run the report in the background as a subprocess.', required=False, default="0", const="1", nargs='?')

  #ALEX-COPYSCRIPT
  parser.add_argument('-init', help='Run the report in the background as a subprocess.', required=False, default=None)

  #This will add arguments for the different tasks
  parseArgs(parser, TASKS)

  args=vars(parser.parse_args())

  setValue = args.get('set_value', None) 
  forKey = args.get('for_key', None) 
  configFileURI = args.get('config', None) 
  version = args.get('v', None)  == "1"
  gracefulExit = args.get('graceful_exit', None)  == "1"
  background = args.get('background', None)  == "1"
  initPfx = args.get('init', None) 

  #process the arguments and see if we're supposed to launch a task.
  taskInfo = getTaskInfo(args, TASKS)

  if(gracefulExit):
    activate(None, gracefulExit=True)

  if(taskInfo != None):

    #If this isn't the -background, then we're going to launch the script on 
    #a subprocess and monitor it with some thread-safe files.
    if(not background):
      activate(taskInfo, args=args, foreground=True)

    #Else, this is the actual task which will be running in the background.
    #Activate the virtual environment, which is going to 
    #perform the installation and setup of the virtual environment
    #and then run the task.
    else:
      activate(taskInfo, background=True)
  
  #Configure the program
  if(configFileURI):
    configure(configFileURI)

  #If we're setting a value in the profile data, then do that here.
  elif(setValue != None and forKey != None):
    setProfileSetting(forKey, setValue)

  elif(initPfx != None):
    init(initPfx)
    
  elif(version):
    versionInfo()

  
  
if __name__ == "__main__":
  main()


