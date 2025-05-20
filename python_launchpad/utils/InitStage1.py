####################################################################################
#
#  A init script to set up a project initially. 
#  The idea is that you put a copy of python-launchpad in your 
#  project to start off with
# 
####################################################################################

from sys import path as syspath 
from python_launchpad.utils.Format import joinPath
from os import path, remove, mkdir
from shutil import move
from python_launchpad.utils.Configure import getLaunchpadDirectory, getSecretsDirectory, getSecretFilesIn, getSecretFilesOut
from python_launchpad.utils.File import replaceInFile, replaceInPlace
from python_launchpad.utils.Utils import readJSON

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))



def init(pfx):

  print("  ")
  print("  ")
  print("****************************************************************************")
  print("** ")
  print("** Python Launchpad: An easy way to create CLI-based")
  print("** monitored tasks and reports.")
  print("** ")
  print("** Building your project area.")
  print("** This script will move a set of files and directories to your project")
  print("** so that you can easily configure your tasks' background and foreground")
  print("** behavior, list dependencies, format arguments and call commmands from")
  print("** your project")
  print("** ")

  #try: 

  lcpfx = pfx.lower()

  launchpadName = 'python_launchpad'

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

  #make the old and new locations of these files
  tasksDir = joinPath(getLaunchpadDirectory(), 'tasks')
  taskFile = joinPath(getLaunchpadDirectory(), 'Tasks.py')
  infoFile = joinPath(getLaunchpadDirectory(), 'Info.py')
  settingsFile = joinPath(getLaunchpadDirectory(), 'settings.json')
  launchpadFile = joinPath(getLaunchpadDirectory(), 'launchpad.py')

  tasksDirDest = joinPath(getLaunchpadDirectory(), '..', f'{lcpfx}_tasks')
  taskFileDest = joinPath(getLaunchpadDirectory(), '..', f'{lcpfx}_task_list.py')
  infoFileDest = joinPath(getLaunchpadDirectory(), '..', f'{lcpfx}_info.py')
  settingsFileDest = joinPath(getLaunchpadDirectory(), '..', f'{lcpfx}_settings.json')
  launchpadFileDest = joinPath(getLaunchpadDirectory(), '..', f'{lcpfx}.py')

  #Here's some files that have imports which will have to change.
  configUtil = joinPath(getLaunchpadDirectory(), 'utils', f'Configure.py')
  venvUtil = joinPath(getLaunchpadDirectory(), 'utils', f'VEnv.py')
  mainFile = joinPath(getLaunchpadDirectory(), 'main.py')

  if(path.isdir(tasksDirDest)):
    print(f"** Directory at {tasksDirDest} already exists")
    print("** ")
  else:
    print(f"** Moving {lcpfx}_tasks directory to your project area")
    print("** This is where your task files live.")
    print("** ")
    move(tasksDir, tasksDirDest)

  if(path.isfile(taskFileDest)):
    print(f"** File at {taskFileDest} already exists")
    print("** ")
  else: 
    print(f"** Moving {lcpfx}_tasks_list.py to your project area")
    print("** This is where you list your tasks.")
    print("** ")

    #We have to do some replacements so that the imports still work.
    replaceInFile(taskFile, taskFileDest, f"{launchpadName}.tasks", f'{lcpfx}_tasks')
    remove(taskFile)

    replaceInPlace(configUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"from {launchpadName}.Info", f"from {lcpfx}_info")
    replaceInPlace(venvUtil, f"tasksModuleName = 'tasks'", f"tasksModuleName = '{lcpfx}_tasks'")
    replaceInPlace(mainFile, f"from {launchpadName}.Tasks", f'from {lcpfx}_task_list')
    replaceInPlace(mainFile, f"project-name-goes-here", lcpfx)

  if(path.isfile(infoFileDest)):
    print(f"** File at {infoFileDest} already exists")
    print("** ")
  else: 
    print(f"** Moving {lcpfx}_info.py to your project area")
    print("** This is where you list the information and dependencies for your project.")
    print("** ")
    move(infoFile, infoFileDest)

  if(path.isfile(launchpadFileDest)):
    print(f"** File at {launchpadFileDest} already exists")
    print("** ")
  else: 
    print(f"** Moving {lcpfx}.py to your project area")
    print(f"** This is the entrypoint for running your commands")
    print("** ")
    move(launchpadFile, launchpadFileDest)

  if(path.isfile(settingsFileDest)):
    print(f"** File at {settingsFileDest} already exists")
    print("** ")
  else: 
    print(f"** Moving {lcpfx}_settings.json to your project area")
    print(f"** This is for configuring your project for the first time")
    print("** ")
    move(settingsFile, settingsFileDest)

  print("** Making secrets directories")
  getSecretsDirectory()
  getSecretFilesIn()
  getSecretFilesOut()

  #Now we're going to rename the launchpad to the new name e.g. "myproj_launchpad"
  projectParentDir = str(getLaunchpadDirectory(asObj=True).parents[0])

  #Make the launchpad data directory.
  launchpadDataDir = joinPath(projectParentDir, f"{lcpfx}_data")
  
  try:
    if(not path.isdir(launchpadDataDir)):
      mkdir(launchpadDataDir)
  except Exception as err:
    raise Exception(f'Could not make the program directory. Did you make a mistake in yout settings file? Here\'s the error: {str(err)}')

  if(path.isdir(joinPath(projectParentDir, 'python_launchpad'))):
    oldProjectDir = joinPath(projectParentDir, 'python_launchpad') 
    newProjectDir = joinPath(projectParentDir, f'{lcpfx}_launchpad')

    if(path.isdir(newProjectDir)):
      raise Exception(f"Cannot change python_launcher to {lcpfx}_launcher. That directory already exists")

    move(oldProjectDir, newProjectDir) 


    print("**")
    print("** Done!")

  # except Exception as err:
  #   print(f"** Error: {str(err)}")

  print("** ")
  print("** ")
  print("****************************************************************************")





