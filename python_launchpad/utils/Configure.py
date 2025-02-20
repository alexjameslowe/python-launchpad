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
from python_launchpad.utils.Format import joinPath
from python_launchpad.Info import PRODUCT_NAME, PRODUCT_NICE_TITLE, VERSION, HELP_EMAIL, AUTHOR

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


####
# get the main settings, which is really just the program_data directory
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
# All of the data that the program needs to run is organized by profile.
#
#
def getDataDirectory():
  launchHandle = getMainSetting("launch_handle")
  return joinPath(getLaunchpadDirectory(), f"{launchHandle}_data")

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
    print(f"Something went wrong. Could not set {value} for key: '{key}': {str(exp)}")


def getPr_ofileSetting(key, _default=None):
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


def configure(jsonURI):

  global mainJSONDataObj, profileJSONDataObj

  try:

    print("**********************************************************")
    print("* ")
    print(f"* Configuring {PRODUCT_NAME}...")
    print(f"* Using settings: {jsonURI}")

    configurationData = readJSON(jsonURI, errorMode=2)
    launchpadHandle = configurationData.get("launchpad_handle")

    if(launchpadHandle == None):
      raise Exception("Missing launchpad_handle in settings")
    

    #mainConfig = configurationData.get('main', None)

    #Configure the main. Get the uri for the program data,
    #and make the folder for it if there isn't already one there.
    #if(mainConfig == None):
    #  raise Exception("No 'main' section of config file")
    
    # programDir = joinPath(getLaunchpadDirectory(), '..', launchpadHandle)
    
    # try:
    #   if(not path.isdir(programDir)):
    #     mkdir(programDir)
    # except Exception as err:
    #   raise Exception(f'Could not make the program directory. Did you make a mistake in yout settings file? Here\'s the error: {str(err)}')

    #fullUserProfileURI = joinPath(programDir, mainUser)
    #if(not path.isdir(fullUserProfileURI)):
    #  mkdir(fullUserProfileURI)

    mainJSONDataObj = configurationData

    writeMainJSON()

    #pythonPath = profileConfig.get("python_location_for_venv", None)
    #systemPython = profileConfig.get("system_python_handle", "python")

    ##Fill in your other things in here.
    
    profileJSONDataObj = {}

    writeProfileJSON()

    print("* Configuration Succeeded!")
    print(f"* You don't need your file '{jsonURI}' anymore.")
    print("* You can get rid of it if you want.")
    print("* From now on you can change the settings by editing:")
    print("* "+joinPath(getDataDirectory(),'profile.json'))
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