import sys 
from os import system, path, mkdir
import importlib
import traceback
from hashlib import sha256
from sys import path as syspath, exc_info

from python_launchpad.utils.Configure import getMainSetting, getDataDirectory, getEnvironmentLevels, getVEnvName, getVenvPath
from python_launchpad.utils.Format import joinPath
from python_launchpad.utils.NonThreadVar import isVar, setVar, getVar, rmVar, setVarsToNormal, setVarsToThreadSafe
from python_launchpad.Info import REQUIREMENTS, BASE_REQUIREMENTS
from python_launchpad.utils.Constants import VENV_ERROR_FLAG
import json
from time import sleep

SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))


def handleException():
  exc_type, exc_value, exc_traceback = exc_info()
  lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
  error_string = ''.join(lines)
  print(error_string)
  return error_string


# Handy way to test if we're in an active venv currently
#vhttps://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
def isVenvActive():
  return sys.prefix != sys.base_prefix


#Have to repeat this here because it doesn't like to do circular imports between Env and Format
def isWindows():
  name = sys.platform.lower()
  return name.startswith('win')


# get the name of the file where the hex digest for the
# environment-specific requirements of this script is stored. 
#
def requirementsHexDigestVarName():
  level0, level1 = getEnvironmentLevels() 
  return f'{level0}_{level1}_requirements_hex_digest'


# Get the path to the requirements file.
#
def getRequirementsFilePath():
  level0, level1 = getEnvironmentLevels()
  return joinPath(getDataDirectory(), f'{level0}_{level1}_requirements.txt')



# Get the requirements list based upon the environment type
#
def getRequirementList():
  requirementList = None 
  level0, level1 = getEnvironmentLevels()

  projectRequirements = REQUIREMENTS[level0][level1]
  baseRequirements = BASE_REQUIREMENTS[level0][level1]
  
  requirementList = projectRequirements + baseRequirements

  return requirementList



# Get the requirements list, sort it and hash it
#
def getRequirementsFileHexHash():

  requirementList = getRequirementList()

  requirementList.sort()
  sortedDependencyString = "__".join(requirementList)

  m = sha256()
  m.update(bytes(sortedDependencyString, 'utf-8'))
  hexdigest = m.hexdigest()

  if(hexdigest == None):
    raise Exception("hexdigest is None for some reason.")
  
  return hexdigest
  

#Refresh the requirements file. It lives in the profile folder, out of the way.
#
def refreshRequirementsFile():

  requirementsList = getRequirementList()

  requirementsPath = getRequirementsFilePath()

  #Clear out the output file. and refresh it with the new requirements.
  with open(requirementsPath, "w+") as f:
    f.write('\n'.join(requirementsList) + '\n')
  


# If this returns None, then we don't need to do the pip install.
# If it's not none, then we DO need to perform a pip install, and in addition
# the return value will be a new hex-digest of the requirements file that has
# to get saved in the requirementsHexDigestVarName() disk variable in the event that
# the installation completes successfully.
#
def doWeNeedToPerformPipInstall(): 

  if(not isVar(requirementsHexDigestVarName())):

    hexDigest = getRequirementsFileHexHash()

    performInstall = True
    return performInstall, hexDigest
  
  else:

    prevHexDigest = getVar(requirementsHexDigestVarName())

    hexDigest = getRequirementsFileHexHash()
    performInstall = False

    if(prevHexDigest != hexDigest):   
      performInstall = True 
      return performInstall, hexDigest

    return performInstall, None
  


#Create the virtual environment if one doesn't already exist.
def createVEnv():

  venvPath = getVenvPath()

  if(not path.isdir(venvPath)):

    pythonPath = getMainSetting("python_location_for_venv", environmental=True)
    systemPython = getMainSetting("system_python_handle", environmental=True)
    level0, level1 = getEnvironmentLevels()

    if(not pythonPath):
      raise Exception(f"Missing python_location_for_venv from settings. Env level0 = {level0}, Env level1 = {level1}")
  
    status = None
    if(isWindows()): 
      print(f'{systemPython} -m virtualenv -p "{joinPath(pythonPath, "python.exe")}" "{venvPath}"')
      status = system(f'{systemPython} -m virtualenv -p "{joinPath(pythonPath, "python.exe")}" "{venvPath}"')
    else:
      print(f'{systemPython} -m virtualenv -p "{pythonPath}" "{venvPath}"')
      status = system(f'{systemPython} -m virtualenv -p "{pythonPath}" "{venvPath}"')

    if(status != 0):
      extra = " I've seen this failure happen on windows machines where Long Path Enabled is false. Google 'Windows enable long paths.'" if isWindows() else ""
      raise Exception(f"Creation of virtual environment failed.{extra}")

    return True 
  
  return False

     
#Install the requirements. If the installation is successful, then we're
#going to update the hex digest of the requirements.txt for idempotence
#(so that we don't re-install the dependencies if we don't have to)
#There is a force parameter that will just make it install it without messing
#around with anything else.
def installRequirements(performInstall, hexDigest, force=False):

  if(force):
    res = system(f'pip install -r "{getRequirementsFilePath()}"')
    if(res != 0):
      raise Exception(f'019384 pip install result was non-zero.')
    return

  if(performInstall):
    refreshRequirementsFile()

    res = system(f'pip install -r "{getRequirementsFilePath()}"')
    if(res != 0):
      raise Exception(f'38437 pip install result was non-zero.')
    
    setVar(requirementsHexDigestVarName(), hexDigest)


# get the base non-persist variables and 
# return a simpe kvp.
#
def getBaseTaskVars():
  return [
    {'name':'ERROR',         'init':'',   'behavior':'output'},
    {'name':'RUNNING',       'init':True, 'behavior':'die'},
    {'name':'STEP',          'init':'',   'behavior':'die'},
    {'name':'WARNING',       'init':'',   'behavior':'output'},
    {'name':'PROCESS',       'init':None, 'behavior':'die'},
    {'name':'GRACEFUL_EXIT', 'init':None, 'behavior':'output'}
  ]


def getVarBehaviors():
  return ['die', 'output', 'persist']


# get the base vars and the vars from the task and merge them
#
def getTaskVars(taskInfo):
  baseAndProjectVars = getBaseTaskVars() + taskInfo.get("vars", [])
  return baseAndProjectVars


# initialize the non-persistent variables to their initial value
# 
def initializeTaskVars(taskInfo):
  allVars = getTaskVars(taskInfo)

  setVarsToThreadSafe()

  for variable in allVars:
    varName = variable['name']
    #This has to be serialized to string or else we get weirdness  
    #When we initialize with 0 of false. TODO iron this out. setVar should be able to just 
    #work in dumb-mode
    varVal = str(variable['init'])
    varBehavior = variable['behavior']
    if(not varBehavior in getVarBehaviors()):
      raise Exception(f'Task: {taskInfo["taskName"]}: The variable {varName} must have a behavior that is one of {",".join(getVarBehaviors())}')
    setVar(varName, varVal)

  setVarsToNormal()


# After a run, we're going to cleanup the threadsafe RUNNING variable
# This used to clean up everything but then I realized that 
# most of the information about the run is useful and you really
# just want to set everything to it default state right before the
# task starts, except for RUNNING and PROCESS which should be 
# cleared out at the end of a task.
#
def cleanupTaskVars(taskInfo, beforeRunOrAfter):
  allVars = getTaskVars(taskInfo)
  
  #we're dealing in the non-thread variables.
  #so we're going to change the state to that it cleans up
  #the thread-safe variables.
  setVarsToThreadSafe()

  #Now, loop through and apply the behaviors
  #If we've started the run, then we're going to zero-out the output variables
  #We're going to zero-out the 'die' variables at the start and end
  #Finally, we're not going to touch the persist variables at all.
  for variable in allVars:
    varName = variable['name']
    varBehavior = variable['behavior']

    if(varBehavior == 'die'):
      rmVar(varName)
    
    elif(varBehavior == 'output' and beforeRunOrAfter):
      rmVar(varName)

  #set the non-thread var utility back to normal.
  setVarsToNormal()


# If we get an error at the end, then this is going
# to write the error out to the output and then send both
# the error and the trace to the ERROR output variable so that
# the monitor will catch it.
#
def handleErrorStrings(traceString, errorMessage):
  print(errorMessage)
  setVarsToThreadSafe()
  setVar('ERROR', f"{errorMessage} \n {traceString}")
  setVarsToNormal()
  

# stop the task from running if there's already one goings.
# 
def bailoutIfRunning():
  setVarsToThreadSafe()
  isRunning = (getVar('RUNNING') == "True")
  setVarsToNormal()
  if(isRunning):
    raise Exception("There's already a task running. Please wait for it to stop.")



# Every now and again, we just need to refresh the dependencies because of some weird thing
# that happens, e.g. this one:
# Version mismatch: this is the 'cffi' package version 1.17.1, located in 'blah/blah/python3.9/site-packages/cffi/api.py'.  
# When we import the top-level '_cffi_backend' extension module, we get version 1.14.0, located in '/usr/lib/python3/dist-packages/_cffi_backend.cpython-38-x86_64-linux-gnu.so'.  
# The two versions should be equal; check your installation.
#
def forceRefreshDependencies():

  print("Refreshing dependencies...")

  if(not isVenvActive()):
    venvPath = getVenvPath()
  
    activate_this = None 

    if(isWindows()):
      activate_this =  joinPath(venvPath, "Scripts", "activate_this.py")
    else:
      activate_this = joinPath(venvPath, "bin", "activate_this.py")

    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    # here's how we activate the virtual environment programmatically.
    # there's no need for a deactivate function. The effects of the activate_this.py
    # only persist for the current run of the script.
    with open(activate_this) as f:
      code = compile(f.read(), activate_this, 'exec')
      exec(code, dict(__file__=activate_this))

    try:
      #pass the force flag and this won't touch the hash file
      installRequirements(None, None, force=True)
    except Exception as err:
      raise Exception(f"694583 {str(err)} Installation failed.")
    
    print("Success!")
  
  else:
    print("Can't run because venv is active.")




# Activate the linux or windows virtual environment
# This is idempotent. If it's already active, this will have no effect.
#
# This won't look like it's activating the venv in any obvious sense. It will activate 
# it for one run of the program. It uses the activate_this.py script instead of 
# the activate binary. It's not really possible/practical to call the activation commands 
# through system() or whatever, particularly if we're trying to install the requirements 
# with pip right after. I think it's better this way anyway. We don't even need a deactivate function.
#
# Literature:
# https://stackoverflow.com/questions/6943208/activate-a-virtualenv-with-a-python-script
# https://stackoverflow.com/questions/13702425/source-command-not-found-in-sh-shell
# https://stackoverflow.com/questions/25559083/is-there-a-way-to-deactivate-a-virtualenv-inside-python-interpreter-i-e-analog
# https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
# https://superuser.com/questions/671372/running-command-in-new-bash-shell-with-rcfile-and-c
# https://stackoverflow.com/questions/6943208/activate-a-virtualenv-with-a-python-script
#
def activate(taskInfo, gracefulExit=False, args=None, background=False, foreground=False, composite=False):

  wasVenvCreated = createVEnv()
  tasksModuleName = 'tasks'

  if(not isVenvActive()):

    venvPath = getVenvPath()
    
    performInstall, hexDigest = doWeNeedToPerformPipInstall()

    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    # here's how we activate the virtual environment programmatically.
    # there's no need for a deactivate function. The effects of the activate_this.py
    # only persist for the current run of the script.
    # then when it's done it will install the requirements in the virtual environment
    
    activate_this = None 

    if(isWindows()):
      activate_this =  joinPath(venvPath, "Scripts", "activate_this.py")
    else:
      activate_this = joinPath(venvPath, "bin", "activate_this.py")

     
    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    # here's how we activate the virtual environment programmatically.
    # there's no need for a deactivate function. The effects of the activate_this.py
    # only persist for the current run of the script.
    with open(activate_this) as f:
      code = compile(f.read(), activate_this, 'exec')
      exec(code, dict(__file__=activate_this))

    try:
      installRequirements(performInstall, hexDigest)
    except Exception as err:
      raise Exception(f"5874 {str(err)} Installation failed.")
    
 
  #If it's a graceful exit, then import in the GracefulExit module and
  #call gracefulExit which will allow the task to know that it's time to exit gracefully.
  if(gracefulExit):
    module = importlib.import_module(f'python_launchpad.utils.GracefulExit')
    module.gracefulExit()
    
  elif(foreground):

    #Launch the subprocesses.
    subprocessLauncher = importlib.import_module(f'python_launchpad.utils.SubprocessLauncher')
    launched = subprocessLauncher.launch(args, taskInfo)

    if(launched):
      #Run the foreground process to monitor the subprocess
      try:
        taskName = taskInfo.get('taskName', None)
        if(taskName == None):
          raise Exception("No taskName.")
        
        module = importlib.import_module(f'{tasksModuleName}.{taskName}.Monitor')
        module.monitor()
      except ModuleNotFoundError as err:
        handleException()
        print(f"Module not found: (0493873) {str(err)}")
      except Exception as err:
        handleException()
        print(f"Monitor error: (119384) {str(err)}")

  elif(background or composite):
    
    #https://github.com/mhammond/pywin32/issues/1865
    #In requirements.txt note that I've pinned the version of pywin32 to 303. Otherwise the one that gets
    #loaded is 228 which is too old and you're going to get this error.
    #Python DLL load failed while importing _win32sysloader The specified module could not be found.txt
    try:

      #Stop the task from running.
      bailoutIfRunning()

      #Cleanup the variables before the run
      cleanupTaskVars(taskInfo, True)

      #Initialize the variables
      initializeTaskVars(taskInfo)

      taskName = taskInfo.get('taskName', None)
      if(taskName == None):
        raise Exception("No taskName.")
      
      #You can raise an exception here to see how it deals with errors.
      #raise Exception("TESTING")
      
      module = importlib.import_module(f'{tasksModuleName}.{taskName}.Task')
      module.task(args)
    except ModuleNotFoundError as err:
      e1 = handleException()
      e2 = f"Module not found: (4746383) {str(err)} {tasksModuleName} {taskName}"
      handleErrorStrings(e1, e2)

    except Exception as err:
      e1 = handleException()
      e2 = f"Task error: (563290) {str(err)}"
      handleErrorStrings(e1, e2)

    #Elean up the variables after the run.
    finally:
      cleanupTaskVars(taskInfo, False)


  
def runModuleInVEnv(modulePackageString):

  createVEnv()

  if(not isVenvActive()):

    venvPath = getVenvPath()

    performInstall = None
    hexDigest = None

    performInstall, hexDigest = doWeNeedToPerformPipInstall()

    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    # here's how we activate the virtual environment programmatically.
    # there's no need for a deactivate function. The effects of the activate_this.py
    # only persist for the current run of the script.
    # then when it's done it will install the requirements in the virtual environment
    
    activate_this = None 

    if(isWindows()):
      activate_this =  joinPath(venvPath, "Scripts", "activate_this.py")
    else:
      activate_this = joinPath(venvPath, "bin", "activate_this.py")

    
    # https://www.a2hosting.com/kb/developer-corner/python/activating-a-python-virtual-environment-from-a-script-file
    # here's how we activate the virtual environment programmatically.
    # there's no need for a deactivate function. The effects of the activate_this.py
    # only persist for the current run of the script.
    with open(activate_this) as f:
      code = compile(f.read(), activate_this, 'exec')
      exec(code, dict(__file__=activate_this))

    try:
      installRequirements(performInstall, hexDigest)
    except Exception as err:
      raise Exception(f"5874 {str(err)} Installation failed.")
     
  module = importlib.import_module(modulePackageString)
  return module

  