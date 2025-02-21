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
from python_launchpad.Info import PRODUCT_NAME, PRODUCT_NICE_TITLE, VERSION, HELP_EMAIL, AUTHOR
#from python_launchpad.utils.VEnv import activate

filePath = path.abspath(path.dirname(__file__))

mainJSONDataObj = None
profileJSONDataObj = None
configureInteractiveMode = False
configureAutoJSONURI = None
configureAutoObject = None

def getHelpMsg():
  return f"If you're having a problem with this script, contact {HELP_EMAIL} for help."

def versionInfo():
  print(f"{PRODUCT_NICE_TITLE}. Version {VERSION} Author {AUTHOR}.") 
  print(f"See README file for details. Email {HELP_EMAIL} with any questions.")

def readMainJSON():
  global mainJSONDataObj
  if(not mainJSONDataObj):

    mainJSONPath = getMain()

    if(path.isfile(mainJSONPath)):
      mainJSONDataObj = readJSON(mainJSONPath)


def readProfileJSON():
  global profileJSONDataObj
  if(not profileJSONDataObj):

    profileJSONPath = getProfile()

    if(path.isfile(profileJSONPath)):
      profileJSONDataObj = readJSON(profileJSONPath)


###
# get the project directory
#
def getLaunchpadDirectory(asObj=False):
  return joinPath(SCRIPT_DIR, "..", asObj=asObj)

##
# get the path to the public key
#
def getPublicKeyPath():
  return joinPath(getDataDirectory(), 'public_key.txt')

##
# get the path to the secrets file where all of the secrets are stored.
#
def getSecretsFilePath():
  return joinPath(getDataDirectory(), 'secrets.json')


####
# get a main setting
#
#
def getMainSetting(key):
  readMainJSON()
  setting = mainJSONDataObj.get(key, None)
  if(setting == None):
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
  

# Get the name of the venv which depends on the platform and the product
#
def getVEnvName():
  name = 'wenv' if isWindows() else 'lenv'
  return f"{name}"

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
  pythonVenvPath = joinPath(getVenvPath(), 'Scripts', 'python.exe') if isWindows() else joinPath(getVenvPath(), 'Scripts', 'python')
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

    #
    # #If the key is the hopper directory, then we're going to make sure
    # #that it exists.
    # if(key == "output_dir"):
    #   outputDirURI = rf"{value}" #For windows slashes
    #   if(not path.isdir(outputDirURI)):
    #     mkdir(outputDirURI)

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

  
  # if(initStage2):
  #   print("Initializing your virtual environment")
  #   activate(initStage2=True, stage2Password='testing123')

