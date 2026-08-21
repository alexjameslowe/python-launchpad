from sys import platform
from os import path 
import sys
from math import isnan
from datetime import date, datetime
from pathlib import PureWindowsPath, PurePosixPath, Path
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



########################################################
#
# Formatting helpers
# author Alex Lowe
#
########################################################

LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


#Have to repeat this here because it doesn't like to do circular imports between Env and Format
def isWindows():
  name = platform.lower()
  return name.startswith('win')

# join path, norm it, and convert it to windows slashes if we're on windows.
# the key word arguments takes the key asObj which is whether or not we return it
# as a string (which is the default behavior)
# 
def joinPath(*args, **kwargs):
  asObj = kwargs.get('asObj', False)
  jPath = path.join(*args)
  nPath = path.normpath(jPath)
  purePath = PureWindowsPath(nPath) if isWindows() else PurePosixPath(nPath)
  #purePath = purePath.replace(" ", "\ ") g/dd/
  joinedPath = purePath if asObj else str(purePath)#.replace(" ", "^ ")

  #There's this problem where uris with " - " fail with the open()
  #function and I can't figure out how to mitigate it. 
  #I love how computers can make videos with prompts 
  #but uris are still a headache.
  # if(isWindows()):
  #   joinedPath = joinedPath.replace(' - ',' \\- ')
  #joinedPath = Path(joinedPath)

  return joinedPath
  #return purePath if asObj else urlparse(str(purePath)).path#.replace(" ", "^ ")


#TODO add some error handling in here for messy strings. Currenly on the honor 
#of the user to get this right.
#turn dash_case like_this_thing to flag-case -like-this-thing
def dashCaseToFlagCase(dashCase):
  return f'-{dashCase.replace("_", "-")}'

#turn flag_case -like-this-thing to dash-case like_this_thing
def flagCaseToDashCase(flagCase):
  return flagCase.replace('-', '_')[1:]


"""Converts a WSL path to a Windows path.

Args:
    wsl_path: The WSL path to convert.

Returns:
    The equivalent Windows path, or None if the conversion fails.
"""
def wslToWindowsPath(wsl_path):
  wsl_path = wsl_path.replace("/mnt/c/", "C:\\")
  wsl_path = wsl_path.replace("/", "\\")
  #wsl_path = wsl_path.replace(" ","^ ")
  return wsl_path
  # try:
  #   if(path.isdir(wsl_path)):
  #     result = subprocess.run(['wslpath', '-w', wsl_path], capture_output=True, text=True, check=True)
  #     windows_path = result.stdout.strip()
  #     return windows_path
  #   return None
  # except subprocess.CalledProcessError:
  #   return None


"""Converts a Windows path to a WSL path.

Args:
    windows_path: The Windows path to convert.

Returns:
    The equivalent WSL path, or None if the conversion fails.
"""
def windowsToWSLPath(windows_path):

  try:
    result = subprocess.run(['wslpath', '-u', windows_path], capture_output=True, text=True, check=True)
    wsl_path = result.stdout.strip()
    return wsl_path
  except subprocess.CalledProcessError:
    return None

#Adapted from
#https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number   
def excelColumn(col):
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)

#Is date a saturday? will default to today
def isDateSaturday(dateObj=None):
  d = dateObj or datetime.today()
  dayOfWeek = d.weekday() # Monday is 0, Sunday is 6
  return dayOfWeek == 5


#Get yyyy-mm-dd from a dateObj or today
def dateToYYYYMMDD(dateObj=None, delimiter="-"):
  if(dateObj == None):
    return datetime.today().strftime(f'%Y{delimiter}%m{delimiter}%d')
  else: 
    return dateObj.strftime(f'%Y{delimiter}%m{delimiter}%d')

# Get yyyy-mm-dd H:M:S with delimiters:
# If dateObj is none, then return now.
# %H: Hour (24-hour clock) as a zero-padded decimal number (00-23).
# %M: Minute as a zero-padded decimal number (00-59).
# %S: Second as a zero-padded decimal number (00-59).
def dateToTimeStamp(dateObj=None, delimiter1="-", delimiter2=" ", delimiter3=":"):
  # Get current date and time
  d = dateObj or datetime.now()

  dl1 = delimiter1
  dl2 = delimiter2
  dl3 = delimiter3

  # Format as YYYY-MM-DD HH:MM:SS with the delimiters
  formatted = d.strftime(f"%Y{dl1}%m{dl1}%d{dl2}%H{dl3}%M{dl3}%S")
  return formatted


#A helper function to get a date object out of a yyyy-mm-dd string
def dateFromYYYYMMDD(yyyymmdd):
  split = yyyymmdd.split('-')
  if(len(split) < 3):
    raise Exception(f"I require a format yyyy-mm-dd. You gave me: {yyyymmdd}")
  yyyy = int(split[0])
  mm = int(split[1])
  dd = int(split[2])

  if(isnan(yyyy)):
    raise Exception(f"The year is malformed. You gave me: {yyyy}")
  if(isnan(mm)):
    raise Exception(f"The month is malformed. You gave me: {mm}")
  if(isnan(dd)):
    raise Exception(f"The day is malformed. You gave me: {dd}")
  
  newDate = date(yyyy, mm, dd)
  return newDate


#A helper to format a string for interpolation into a CLI string
def formatForCLI(dirty, escapeSingleQuote=False, escapeDoubleQuote=False, removeSingleQuote=False, removeDoubleQuote=False):
  clean = dirty
  if(escapeSingleQuote):
    clean = clean.replace("'", "\\'")
  if(escapeDoubleQuote):
    clean = clean.replace('"', '\\"')
  if(removeSingleQuote):
    clean = clean.replace("'", "")
  if(removeDoubleQuote):
    clean = clean.replace('"',"")

  return clean

# https://stackoverflow.com/questions/16807011/python-how-to-identify-if-a-variable-is-an-array-or-a-scalar
def isEmptyArray(x):
  if hasattr(x, '__len__') and (not isinstance(x, str) and len(x) == 0):
    return True 
  return False