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
from os import path, rename, system
import subprocess
from time import time
from shutil import copy
from python_launchpad.utils.Configure import getLaunchpadDirectory, getDataDirectory
from python_launchpad.utils.File import replaceInPlace, rename as xrename
from python_launchpad.utils.Utils import readJSON
import requests 
import zipfile


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))


def downloadFile(url, localURI):
  try:
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Raise an exception for non-200 status codes

    with open(localURI, 'wb') as file:
        for chunk in response.iter_content(chunk_size=8192):
            file.write(chunk)

  except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")


# https://stackoverflow.com/questions/3451111/unzipping-files-in-python
def unzip(zipURI, extractionDir):
  with zipfile.ZipFile(zipURI, 'r') as zip_ref:
      zip_ref.extractall(extractionDir)


def upgrade(pfx):

  currentMasterURI = 'https://github.com/alexjameslowe/python-launchpad/archive/refs/heads/master.zip'

  downloadFile(currentMasterURI)

  lcpfx = pfx.lower()
  projectParentDir = str(getLaunchpadDirectory(asObj=True).parents[0])
  oldProjectDir = joinPath(projectParentDir, f'{lcpfx}_launchpad')
  backupDir = joinPath(getDataDirectory(), f'{lcpfx}_launchpad_backup')

  print("  ")
  print("  ")
  print("****************************************************************************")
  print("** ")
  print("** Python Launchpad: An easy way to create CLI-based")
  print("** monitored tasks and reports.")
  print("** ")
  print("** Upgrading with this new launchpad.")
  print("** This script will use your current tasks, data and secrets")
  print(f"** and replace your current {lcpfx}_launchpad with this new one.")
  print("** ")

  launchpadName = 'python_launchpad'
    
  if(not path.isdir(oldProjectDir)): 
    raise Exception("There is no launchpad called: {lcpfx}_launchpad")
  
  try:
  
    # https://stackoverflow.com/questions/67362152/issues-with-os-rename-getting-winerror-5-access-is-denied
    print("** Backing up the old launchpad")    
    if(path.isdir(backupDir)):
      xrename(backupDir, backupDir+"_"+str(int(time())))

    xrename(oldProjectDir, backupDir)

    #Loop through the whole manifest of files and we're going to change
    #all of the instances of 'python_launchpad' to the the new name e.g. myproj_launchpad
    fileManifest = readJSON(joinPath(getLaunchpadDirectory(), 'manifest.json'))
    for file in fileManifest:
      try:
        if(file == "settings.json"):
          file = joinPath(getLaunchpadDirectory(), file)
          replaceInPlace(file, "python_launchpad", lcpfx)
        else:
          file = joinPath(getLaunchpadDirectory(), file)
          replaceInPlace(file, "python_launchpad", f"{lcpfx}_launchpad")
      except:
        raise Exception(f"Error: could not perform replacements on {file}")

    #Record this because we have to make more changes to the packaging
    #when we start moving files out of the launchpad to your workspace.
    #These further replacements are below:
    launchpadName = f"{lcpfx}_launchpad"

    #Here's some files that have imports which will have to change.
    configUtil = joinPath(getLaunchpadDirectory(), 'utils', f'Configure.py')
    venvUtil = joinPath(getLaunchpadDirectory(), 'utils', f'VEnv.py')
    mainFile = joinPath(getLaunchpadDirectory(), 'main.py')

    replaceInPlace(configUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"tasksModuleName = 'tasks'", f"tasksModuleName = '{lcpfx}_tasks'")
    replaceInPlace(mainFile, f"from {launchpadName}.Tasks", f'from {lcpfx}_task_list')
    replaceInPlace(mainFile, f"project-name-goes-here", lcpfx)

    print("** Installing the new launchpad")
    #and now change the name of the launch pad to the new one.
    launchpadDir = joinPath(projectParentDir, 'python_launchpad') 
    newProjectDir = joinPath(projectParentDir, f'{lcpfx}_launchpad')

    xrename(launchpadDir, newProjectDir)

    print("** Copying settings")
    settingsFileFromOld = joinPath(backupDir, 'main.json')
    copy(settingsFileFromOld, newProjectDir) 

    print("**")
    print("** Done!")

  except Exception as e: 
    print("**")
    print(f"** Error: {str(e)}")
    print("**")
    print("** Could not complete. Delete this python_launchpad and try a fresh copy.")

  finally:

    print("** ")
    print("** ")
    print("****************************************************************************")





