from sys import platform
from os import path 
import sys
from math import isnan
from datetime import date
from pathlib import PureWindowsPath, PurePosixPath, Path

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


#Adapted from
#https://stackoverflow.com/questions/19153462/get-excel-style-column-names-from-column-number   
def excelColumn(col):
    result = []
    while col:
        col, rem = divmod(col-1, 26)
        result[:0] = LETTERS[rem]
    return ''.join(result)


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