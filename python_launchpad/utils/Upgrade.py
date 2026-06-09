#git@github.com:alexjameslowe/python-launchpad.git

####################################################################################
#
#  An upgrade script.
#  What you do is you get a new copy of python_launchpad,
#  you put it in your project directory alongside your current one
#  and then you run the main.py with the -update "myproject"
# 
####################################################################################

from sys import path as syspath 
from python_launchpad.utils.Format import joinPath
from os import path, rename, system, mkdir
import subprocess
from time import time
from shutil import copy, copytree, move, rmtree
from python_launchpad.utils.Configure import getLaunchpadDirectory, getDataDirectory
from python_launchpad.utils.File import replaceInPlace, rename as xrename
from python_launchpad.utils.Utils import readJSON
from python_launchpad.utils.NonThreadVar import getVar
from python_launchpad.utils.Constants import ORIGINAL_NAME
import requests 
import zipfile
import json


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))


#This will expand it to <your_proj>_data/python-launchpad-master/python-launchpad-master/python_launchpad
def downloadMasterBranchToData():

  localZipURI = joinPath(getDataDirectory(), 'python-launchpad.zip')
  localExpandToURI = joinPath(getDataDirectory(), 'python-launchpad-master')
  masterBranchRemoteZipURL = 'https://github.com/alexjameslowe/python-launchpad/archive/refs/heads/master.zip'

  # https://stackoverflow.com/questions/3451111/unzipping-files-in-python
  # https://www.codementor.io/@aviaryan/downloading-files-from-urls-in-python-77q3bs0un
  response = requests.get(masterBranchRemoteZipURL, allow_redirects=True)
  open(localZipURI, 'wb').write(response.content)

  if(path.isdir(localExpandToURI)):
    rmtree(localExpandToURI)

  if(not path.isdir(localExpandToURI)):
    mkdir(localExpandToURI)

  with zipfile.ZipFile(localZipURI, 'r') as zip_ref:
      zip_ref.extractall(localExpandToURI)


def upgrade(pfx):

  #currentMasterURI = getVar('master-branch-uri').strip()
  #downloadFile(currentMasterURI)

  ##This will expand it to <your_proj>_data/python-launchpad-master/python-launchpad-master/python_launchpad
  downloadMasterBranchToData()

  lcpfx = pfx.lower()
  projectParentDir = str(getLaunchpadDirectory(asObj=True).parents[0])
  oldProjectDir = joinPath(projectParentDir, f'{lcpfx}_launchpad')
  backupDir = joinPath(getDataDirectory(), f'{lcpfx}_launchpad_backup')

  #and now change the name of the launch pad to the new one.
  launchpadDir = joinPath(projectParentDir, ORIGINAL_NAME) 
  newLaunchpadDir = joinPath(projectParentDir, f'{lcpfx}_launchpad')

  print("  ")
  print("  ")
  print("****************************************************************************")
  print("** ")
  print("** Python Launchpad: An easy way to create CLI-based")
  print("** monitored tasks and reports.")
  print("** ")
  print("** Upgrading with this new launchpad.")
  print("** This script will use your current tasks, data and secrets")
  print(f"** and replace your current {lcpfx}_launchpad with the current.")
  print("** master branch.")
  print("** ")

  launchpadName = 'python_launchpad'
    
  if(not path.isdir(oldProjectDir)): 
    raise Exception(f"There is no launchpad called: {lcpfx}_launchpad: This is not a directory: {oldProjectDir}")
  
  try:

    print("** Fetching new master")

    newCopiedPythonLauncpadFromMasterURI = joinPath(getDataDirectory(), 'python-launchpad-master', 'python-launchpad-master', 'python_launchpad')

    #Make a copy of the master branch and place it the parent of the launchpad directory.
    copytree(newCopiedPythonLauncpadFromMasterURI, joinPath(projectParentDir, ORIGINAL_NAME), dirs_exist_ok=True)

    print("** Performing replacments")

    #Loop through the whole manifest of files and we're going to change
    #all of the instances of 'python_launchpad' to the the new name e.g. myproj_launchpad
    fileManifest = readJSON(joinPath(launchpadDir, 'manifest.json'))
    for file in fileManifest:
      try:
        if(file == "settings.json"):
          file = joinPath(launchpadDir, file)
          replaceInPlace(file, ORIGINAL_NAME, lcpfx)
        else:
          file = joinPath(launchpadDir, file)
          replaceInPlace(file, ORIGINAL_NAME, f"{lcpfx}_launchpad")
      except:
        raise Exception(f"Error: could not perform replacements on {file}")
      
    #Record this because we have to make more changes to the packaging
    #when we start moving files out of the launchpad to your workspace.
    #These further replacements are below:
    launchpadName = f"{lcpfx}_launchpad"

    #Here's some files that have imports which will have to change.
    configUtil = joinPath(launchpadDir, 'utils', f'Configure.py')
    venvUtil = joinPath(launchpadDir, 'utils', f'VEnv.py')
    mainFile = joinPath(launchpadDir, 'main.py')

    replaceInPlace(configUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"tasksModuleName = 'tasks'", f"tasksModuleName = '{lcpfx}_tasks'")
    replaceInPlace(mainFile, f"from {launchpadName}.Tasks", f'from {lcpfx}_task_list')
    replaceInPlace(mainFile, f"project-name-goes-here", lcpfx)

    print("** Moving directories")

    # https://stackoverflow.com/questions/67362152/issues-with-os-rename-getting-winerror-5-access-is-denied
    print("** Backing up the old launchpad")    
    if(path.isdir(backupDir)):
      move(backupDir, backupDir+"_"+str(int(time())))

    move(oldProjectDir, backupDir)

    print("** Renaming directory")
    move(launchpadDir, newLaunchpadDir)

    print("** Copying settings")
    settingsFileFromOld = joinPath(backupDir, 'main.json')
    copy(settingsFileFromOld, newLaunchpadDir) 

    print("**")
    print("** Done!")

  except Exception as e: 
    print("**")
    print(f"** Error: {str(e)}")
    print("**")
    print("** Could not complete.")

  finally:

    print("** ")
    print("** ")
    print("****************************************************************************")





