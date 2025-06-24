import os
import argparse, sys
from os import path

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Configure import configure, setProfileSetting, versionInfo
from python_launchpad.utils.VEnv import activate, runModuleInVEnv, cleanupNonPersistVars, forceRefreshDependencies
from python_launchpad.utils.TaskHelper import parseArgs, getTaskInfo
from python_launchpad.utils.InitStage1 import init
from python_launchpad.utils.Upgrade import upgrade
from python_launchpad.Tasks import TASKS

PROJECT_LC_NAME = 'project-name-goes-here'

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
  parser.add_argument('-config', help='Configure the program.', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-test', help='Is this a test?', required=False, default="0", const="1", nargs='?')
  
  parser.add_argument('-set-value', help='Whats the value of the setting youd like to set?', required=False, default=None)
  
  parser.add_argument('-set-secret', help='What secret do you want to save?', required=False, default=None)
  parser.add_argument('-get-secret', help='You want to get a secret?', required=False, default="0", const="1", nargs='?')
  
  parser.add_argument('-for-key', help='Which key do you want to set the value for?', required=False, default=None)
  
  parser.add_argument('-list-secrets', help='List the names of the secrets', required=False, default="0", const="1", nargs='?')

  parser.add_argument('-v', help='Get version info', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-graceful-exit', help='Do you want to exit gracefully?', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-background', help='Run the report in the background as a subprocess.', required=False, default="0", const="1", nargs='?')

  parser.add_argument('-init', help='Initialize the project', required=False, default=None)
  parser.add_argument('-upgrade', help='Upgrade the project with a new launchpad', required=False, default=None)
  parser.add_argument('-cleanup-task', help='Clean up after a task has failed in an ungraceful fashion like a crash', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-refresh-deps', help='Refresh the dependencies', required=False, default="0", const="1", nargs='?')
  
  parser.add_argument('-wsl-bridge-generate-keys', required=False, default="0", const="1", nargs='?')
  parser.add_argument('-wsl-bridge-get-private-key', required=False, default="0", const="1", nargs='?')


  #This will add arguments for the different tasks
  parseArgs(parser, TASKS)

  args=vars(parser.parse_args())

  setValue = args.get('set_value', None) 
  setSecret = args.get('set_secret', None) 
  getSecret = args.get('get_secret', None) == "1"
  forKey = args.get('for_key', None) 

  config = args.get('config', None) == "1"
  version = args.get('v', None) == "1"
  gracefulExit = args.get('graceful_exit', None) == "1"
  background = args.get('background', None) == "1"
  initProjectHandle = args.get('init', None) 
  upgradeProjectHandle = args.get('upgrade', None)
  listSecrets = args.get('list_secrets', None) == "1"
  wslBridgeGenerateKeys = args.get("wsl_bridge_generate_keys", None) == "1"
  wslBridgeGetPrivateKey = args.get("wsl_bridge_get_private_key", None) == "1"
  cleanupTask =  args.get("cleanup_task", None) == "1"
  refreshDeps = args.get("refresh_deps", None) == "1"

  taskInfo = None

  #process the arguments and see if we're supposed to launch a task.
  taskInfo = getTaskInfo(args, TASKS)

  composite = False 
  if(taskInfo != None):
    composite = taskInfo.get('composite', False)

  if(gracefulExit):
    activate(None, gracefulExit=True)

  if(taskInfo != None):

    #If we're supposed to cleanup after a task because something went wrong,
    #then we're going to run this
    if(cleanupTask):
      cleanupNonPersistVars(taskInfo)

    #Else, we're going to run the task, handling a couple of different modes.
    else:

      # #If this is composite, then that means that we're going to just run it 
      # in the foreground 
      if(composite):
        activate(taskInfo, args=args, composite=True)

      #If this isn't the -background, then we're going to launch the script on 
      #a subprocess and monitor it with some thread-safe files.
      elif(not background):
        activate(taskInfo, args=args, foreground=True)

      #Else, this is the actual task which will be running in the background.
      #Activate the virtual environment, which is going to 
      #perform the installation and setup of the virtual environment
      #and then run the task.
      else:
        activate(taskInfo, args=args, background=True)
  
  #Configure the program
  if(config):
    configFileURI = path.abspath(path.join(path.dirname(__file__), "..", f"{PROJECT_LC_NAME}_settings.json"))
    configure(configFileURI)

    module = runModuleInVEnv('python_launchpad.utils.InitStage2')
    module.init()

  #refresh the dependencies
  elif(refreshDeps != None):
    forceRefreshDependencies()

  #If we're setting a value in the profile data, then do that here.
  elif(setValue != None and forKey != None):
    setProfileSetting(forKey, setValue)

  elif(setSecret != None and forKey != None):
    secrets = runModuleInVEnv('python_launchpad.utils.Secrets')
    secrets.setSecret(forKey, setSecret)

  elif(getSecret and forKey != None):
    secrets = runModuleInVEnv('python_launchpad.utils.Secrets')
    print(f"secret for '{forKey}': ")
    print(secrets.getSecret(forKey))

  elif(listSecrets): 
    secrets = runModuleInVEnv('python_launchpad.utils.Secrets')
    secrets.listSecrets()

  elif(initProjectHandle != None):
    init(initProjectHandle)

  elif(upgradeProjectHandle != None):
    upgrade(upgradeProjectHandle)

  elif(wslBridgeGenerateKeys):
    secrets = runModuleInVEnv('python_launchpad.utils.Secrets')
    secrets.generateKeys()  

  elif(wslBridgeGetPrivateKey):
    secrets = runModuleInVEnv('python_launchpad.utils.Secrets')
    pkey = secrets.getPrivateKey()  
    print(pkey)
    
  elif(version):
    versionInfo()

  
  
if __name__ == "__main__":
  main()


