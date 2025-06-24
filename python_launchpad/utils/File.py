from os.path import exists 
from os import path, remove, rename as osrename
from shutil import move 
from python_launchpad.utils.Format import isWindows, wslToWindowsPath
import sys
import subprocess


# getting the name of the directory
# where the this file is present.
current = path.dirname(path.realpath(__file__))
# Getting the parent directory name
# where the current directory is present.
parent = path.dirname(current)
# adding the parent directory to
# the sys.path.
sys.path.append(parent)



def removeIfExists(uriPath):
  if exists(uriPath):
    remove(uriPath)

#https://stackoverflow.com/questions/4128144/replace-string-within-file-contents
def replaceInFile(infileURI, outfileURI, searchFor, replaceWith):
  with open(infileURI, "rt") as fin:
    with open(outfileURI, "wt") as fout:
        for line in fin:
            fout.write(line.replace(searchFor, replaceWith))

def replaceInPlace(infileURI, searchFor, replaceWith):
  oldFile = infileURI
  newFile = f"{infileURI}.xyz"
  replaceInFile(oldFile, newFile, searchFor, replaceWith)
  remove(oldFile)
  move(newFile, oldFile)


#Rename a directory or file.
#On Windows, renaming things will give you all kinds of terrible problems.
#just do it this way if windows. Don't even bother with the os.rename.
#
def rename(oldDir, newDir):
  if(isWindows()):
    subprocess.run(["powershell", "Rename-Item", "-Path", f'"{wslToWindowsPath(oldDir)}"', "-NewName", f'"{wslToWindowsPath(newDir)}"'])
  else:
    osrename(oldDir, newDir)
