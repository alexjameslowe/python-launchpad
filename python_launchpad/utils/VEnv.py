import sys 
from os import system, path, mkdir
import importlib
import traceback
from hashlib import sha256
from sys import path as syspath, exc_info

from python_launchpad.utils.Configure import getMainSetting, getDataDirectory
from python_launchpad.utils.Format import joinPath, getEnvironmentLevel0, getEnvironmentLevel1
from python_launchpad.utils.NonThreadVar import isVar, setVar, getVar
from python_launchpad.Info import REQUIREMENTS, BASE_REQUIREMENTS

SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))


def handleException():
  exc_type, exc_value, exc_traceback = exc_info()
  lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
  error_string = ''.join(lines)
  print(error_string)


# Handy way to test if we're in an active venv currently
#vhttps://stackoverflow.com/questions/1871549/determine-if-python-is-running-inside-virtualenv
def isVenvActive():
  return sys.prefix != sys.base_prefix

#Have to repeat this here because it doesn't like to do circular imports between Env and Format
def isWindows():
  name = sys.platform.lower()
  return name.startswith('win')


# get both enviornment levels
#
def getEnvironmentLevels():
  level0 = getEnvironmentLevel0() 
  level1 = getEnvironmentLevel1()
  return level0, level1


# get the name of the file where the hex digest for the
# environment-specific requirements of this script is stored. 
#
def requirementsHexDigestVarName():
  level0, level1 = getEnvironmentLevels() 
  return f'{level0}_{level1}_requirments_hex_digest'


# Get the name of the venv which depends on the 
# level0 (base environment) and level1 (type of environment)
#
def getVEnvName():
  venvName = f"venv_{getEnvironmentLevel0()}_{getEnvironmentLevel1()}"
  return venvName


# Get the path to the requirements file.
#
def getRequirementsFilePath():
  level0 = getEnvironmentLevel0() 
  level1 = getEnvironmentLevel1()
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
  

def getVenvPath():
  dataDirectory = getDataDirectory()
  venvName = getVEnvName()
  venvPath = joinPath(dataDirectory, venvName)

  return venvPath  


#Create the virtual environment if one doesn't already exist.
def createVEnv():

  venvPath = getVenvPath()

  if(not path.isdir(venvPath)):

    pythonPath = getMainSetting("python_location_for_venv", environmental=True)
    systemPython = getMainSetting("system_python_handle", environmental=True)

    if(not pythonPath):
      raise Exception(f"Missing python_location_for_venv from settings. Env level0 = {getEnvironmentLevel0()}, Env level1 = {getEnvironmentLevel1()}")
  
    if(isWindows()):
      system(f'{systemPython} -m virtualenv -p "{joinPath(pythonPath, "python.exe")}" "{venvPath}"')
    else:
      system(f'{systemPython} -m virtualenv -p "{pythonPath}" "{venvPath}"')

    return True 
  
  return False

     
#Install the requirements. If the installation is successful, then we're
#going to update the hex digest of the requirements.txt for idempotence
#(so that we don't re-install the dependencies if we don't have to)
def installRequirements(performInstall, hexDigest):
  if(performInstall):
    refreshRequirementsFile()

    res = system(f'pip install -r "{getRequirementsFilePath()}"')
    if(res != 0):
      raise Exception(f'38437 pip install result was non-zero.')
    
    setVar(requirementsHexDigestVarName(), hexDigest)



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

    performInstall = None
    hexDigest = None
    
    if(not wasVenvCreated):
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
      except Exception as err:
        handleException()
        print(f"Module not found: (0493873) {str(err)}")


  elif(background or composite):
    
    #https://github.com/mhammond/pywin32/issues/1865
    #In requirements.txt note that I've pinned the version of pywin32 to 303. Otherwise the one that gets
    #loaded is 228 which is too old and you're going to get this error.
    #Python DLL load failed while importing _win32sysloader The specified module could not be found.txt
    try:
      taskName = taskInfo.get('taskName', None)
      if(taskName == None):
        raise Exception("No taskName.")

      module = importlib.import_module(f'{tasksModuleName}.{taskName}.Task')
      module.task(args)
    except Exception as err:
      handleException()
      print(f"Module not found: (4746383) {str(err)} {tasksModuleName} {taskName}")


  
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

  