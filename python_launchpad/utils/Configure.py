import json
from os import path, mkdir
import sys


########################################################
#
# Configuration utilities
# author Alex Lowe
#
########################################################


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Utils import readJSON 
from python_launchpad.utils.Format import joinPath, isWindows
from python_launchpad.Info import PRODUCT_NAME, PRODUCT_NICE_TITLE, VERSION, HELP_EMAIL, AUTHOR, RESOLVE_LINUX_ENVIRONMENT, RESOLVE_MAC_ENVIRONMENT, RESOLVE_WINDOWS_ENVIRONMENT

from sys import platform
from uuid import uuid4


filePath = path.abspath(path.dirname(__file__))

ENV_WINDOWS = 'windows'
ENV_LINUX = 'linux'
ENV_MAC = 'mac'

mainJSONDataObj = None
profileJSONDataObj = None
configureInteractiveMode = False
configureAutoJSONURI = None
configureAutoObject = None

## 
# Check to see if a keyring backend is being used.
#
def getKeyringBackendStatus():
 
  useKeyringBackend = getMainSetting('keyring_backend', True, True) 
   
  #If we're skipping the keyring backend, then we just read the private key from the file.
  #We're treating None as true for background compatibility
  if(useKeyringBackend == False and useKeyringBackend != None):
    return False 
  
  return True


def readMainJSON():
  global mainJSONDataObj
  if(not mainJSONDataObj):

    mainJSONPath = getMain()

    if(path.isfile(mainJSONPath)):
      mainJSONDataObj = readJSON(mainJSONPath)
    else: 
      raise Exception(f"Main configuration file not found at {mainJSONPath}")


def readProfileJSON():
  global profileJSONDataObj
  if(not profileJSONDataObj):

    profileJSONPath = getProfile()

    if(path.isfile(profileJSONPath)):
      profileJSONDataObj = readJSON(profileJSONPath)


#get the base environment, which is either
#windows, mac or linux.
def getEnvironmentLevel0():
  name = platform.lower() 
  level0 = None
  if(name.startswith("win")):
    level0 = ENV_WINDOWS
  elif(name == "darwin"):
    level0 = ENV_MAC
  else:
    level0 = ENV_LINUX

  if(not level0):
    raise Exception(f"I don't know what kind of environment this is. Here's the platform string: {name}")
  
  return level0 


#From the level0 environment type, get the level1 type.
#These two types will be used to resolve dependencies 
#and figure out which virtual enviornment we're supposed to be
#using.
def getEnvironmentLevel1():
  level0 = getEnvironmentLevel0()
  level1 = None
  if(level0 == ENV_WINDOWS):
    level1 = RESOLVE_WINDOWS_ENVIRONMENT()
  elif(level0 == ENV_MAC):
    level1 = RESOLVE_MAC_ENVIRONMENT()
  elif(level0 == ENV_LINUX):
    level1 = RESOLVE_LINUX_ENVIRONMENT() 
  
  if(not level1):
    raise Exception(f"I was not able to find a level-1 environment type for this {level0} environment, i.e., I know that maybe its a linux environment but I don't know WHICH linux.")

  return level1


# get both enviornment levels
#
def getEnvironmentLevels():
  level0 = getEnvironmentLevel0() 
  level1 = getEnvironmentLevel1()
  return level0, level1



###
# get the project directory
#
def getLaunchpadDirectory(asObj=False):
  return joinPath(SCRIPT_DIR, "..", asObj=asObj)

##
# get the path to the public key
#
def getPublicKeyPath():
  return joinPath(getSecretsEncryptedDirectory(), 'public_key.txt')

## 
# get the path to the secrets directory
#
def getSecretsDirectory():
  dir = joinPath(getProjectDirectory(), f'{getMainSetting("launchpad_handle")}_secrets', 'encrypted') 
  if(not path.isdir(dir)):
    mkdir(dir) 
  
  return dir

##
# get the secrets/encrypted directory
#
def getSecretsEncryptedDirectory():
  secretsDir = getSecretsDirectory()
  encryptedDir = joinPath(secretsDir, 'encrypted')
  if(not path.isdir(encryptedDir)):
    mkdir(encryptedDir) 
  
  return encryptedDir


## 
# get the path to the secret files input directory
#
def getSecretFilesIn():
  secretsDir = getSecretsDirectory()
  dir = joinPath(secretsDir, 'files_in') 
  if(not path.isdir(dir)):
    mkdir(dir) 
  
  return dir

## 
# get the path to the secret files output directory
#
def getSecretFilesOut():
  secretsDir = getSecretsDirectory()
  dir = joinPath(secretsDir, 'files_out') 
  if(not path.isdir(dir)):
    mkdir(dir) 
  
  return dir


## 
# get the path to the secrets directory
#
def getSecretsManifest():
  manifestURI = joinPath(getSecretsEncryptedDirectory(), 'manifest.json')
  return manifestURI
  

##
# get the path to the project directory.
#
def getProjectDirectory(asObj=False):
  return joinPath(getLaunchpadDirectory(), '..', asObj=asObj)



####
# get a main setting
#
#
def getMainSetting(key, environmental=False, defaultToNone=False):
  readMainJSON()

  #just read the top-level settings if it's not from
  #the environmental data
  if(not environmental):
    try:
      setting = mainJSONDataObj.get(key, None)
      if(setting == None):
        if(defaultToNone):
          return None 
        else:
          raise Exception(f"No setting for '{key}'. Did you run with the -config flag yet?")
      else:
        return setting 
    except Exception as err:
      raise Exception(f"Could not get main setting for key '{key}': {str(err)}")
  
  #else, if its specific to the environment, then we're
  #going to get the level0 and level1 environment types
  #and dig into the settings to find the information.
  else: 
    level0 = getEnvironmentLevel0() 
    level1 = getEnvironmentLevel1()
    specific = mainJSONDataObj[level0][level1]
    setting = specific.get(key, None) 
    if(setting == None):
      if(defaultToNone):
        return None 
      else:
        raise Exception(f"No setting for '{key}'. Did you run with the -config flag yet?")
    else: 
      return setting

####
# set a main setting
#
#
def setMainSetting(key, value):
  try:

    readMainJSON()
    mainJSONDataObj[key] = value
    writeMainJSON()

    print(f"Set {value} for key: '{key}'")

  except Exception as err:
    print(f"695849 Something went wrong. Could not set {value} for key: '{key}': {str(err)}")




####
# All of the data that the program needs to run is organized by profile.
#
#
def getDataDirectory():
  launchHandle = getMainSetting("launchpad_handle")
  return joinPath(getLaunchpadDirectory(), '..', f"{launchHandle}_data")


####
# Return the profile uri for the user
#
#
def getProfile():
  return joinPath(getDataDirectory(), "profile.json") 


###
# Return main uri
#
def getMain():
  return joinPath(SCRIPT_DIR, '..', 'main.json')
  

# Get the name of the venv which depends on the 
# level0 (base environment) and level1 (type of environment)
#
def getVEnvName():
  venvName = f"venv_{getEnvironmentLevel0()}_{getEnvironmentLevel1()}"
  return venvName


##
# Get the path to the venv
#
def getVenvPath():
  dataDirectory = getDataDirectory()
  venvName = getVEnvName()
  venvPath = joinPath(dataDirectory, venvName)
  return venvPath  


##
# get the path to the python executable
#
#
def getPythonExecutable():  
  pythonVenvPath = None 
  if(isWindows()):
    pythonVenvPath = joinPath(getVenvPath(), 'Scripts', 'python.exe') 

  #For everyone else, you just use "python"  
  else:
    pythonVenvPath = "python"
    
  return pythonVenvPath


#####
# getter and setter for the profile settings.
#
#
def setProfileSetting(key, value):
  try:
      
    readProfileJSON()
    profileJSONDataObj[key] = value 
    writeProfileJSON()

    print(f"Set {value} for key: '{key}'")

  except Exception as exp:
    print(f"030495 Something went wrong. Could not set {value} for key: '{key}': {str(exp)}")


def getProfileSetting(key, _default=None):
  readProfileJSON()
  return profileJSONDataObj.get(key, _default)


####
# Write the profile 
#
#
def writeProfileJSON():
  profileJSONPath = getProfile()

  with open(profileJSONPath, 'w') as jsonFile:
    json.dump(profileJSONDataObj, jsonFile)
    jsonFile.close()

  
####
# Write the main json config
#
#
def writeMainJSON():
  with open(getMain(), 'w') as jsonFile:
    json.dump(mainJSONDataObj, jsonFile)
    jsonFile.close()

###
# get the of the of the launchpad. If there's a uid, then use it. 
#
#
def getServiceName():
  launchHandle = getMainSetting("launchpad_handle", False, True)
  uid = getMainSetting("uuid", False, True)

  if(launchHandle == None):
    raise Exception("launchpad_handle is missing fro the main config json")
  
  if(uid == None): 
    return f'{launchHandle}_launchpad'
  else: 
    return f'{launchHandle}_launchpad_{uid}'

##
# get the username. 
#
#
def getUsername():
  return "default_user"

##
# get the help message   
#
def getHelpMsg():
  return f"If you're having a problem with this script, contact {HELP_EMAIL} for help."

###
# Print out info 
#
def versionInfo():
  print(f"{PRODUCT_NICE_TITLE}. Version {VERSION} Author {AUTHOR}.") 

  if(getKeyringBackendStatus()):
    print("Using keyring backend for secrets.")
  else:
    print("Not using keyring backend for secrets. Using file system instead.")

  print(f"Environment: {getEnvironmentLevel0()}-{getEnvironmentLevel1()}")
  print(f"Service name: {getServiceName()}")
  print(f"See README file for details. Email {HELP_EMAIL} with any questions.")



###
# run the configuration with the given json file.
#
#
def configure(jsonURI=None):

  global mainJSONDataObj, profileJSONDataObj

  try:
      
    print("**********************************************************")
    print("* ")
    print(f"* Configuring {PRODUCT_NAME}...")

    if(path.isfile(getMain())):

      print("* It looks like the launcher was already configured.")
      print("* ")
      print("**********************************************************")

    else:

      print(f"* Using settings: {jsonURI}")

      configurationData = readJSON(jsonURI, errorMode=2)
      launchpadHandle = configurationData.get("launchpad_handle")

      if(launchpadHandle == None):
        raise Exception("Missing launchpad_handle in settings")
      
      mainJSONDataObj = configurationData
      mainJSONDataObj['uuid'] = str(uuid4())

      writeMainJSON()

      ##Fill in your other things in here.
      
      profileJSONDataObj = {}

      writeProfileJSON()

      print("* Configuration Succeeded!")
      print(f"* You don't need your file '{jsonURI}' anymore.")
      print("* You can get rid of it if you want.")
      print("* From now on you can change the settings by editing:")
      print("* "+getMain())
      print("* ")
      # print more stuff here about the output directory or whatever.
      print("* ")
      print("* ")
      print("**********************************************************")

  except Exception as err:
    print(f"* Error: Could not configure: {str(err)}")
    print("* "+getHelpMsg())
    print("* ")
    print("**********************************************************")

  

