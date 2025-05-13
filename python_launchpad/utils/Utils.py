import sys
from os import path
import json
import re
import datetime 
import random 
import string


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))


#https://stackoverflow.com/questions/16807011/python-how-to-identify-if-a-variable-is-an-array-or-a-scalar
def isArray(value):
  return hasattr(value, '__len__') and (not isinstance(value, str))


#Get a random string with a date-string prepended so collision chances go to zero
#unless you're using this a million times a second and you get really unlucky.
def randomString(length=8):
  """Generates a random string that incorporates the current date."""
  now = datetime.datetime.now()
  date_string = now.strftime("%Y%m%d%H%M%S")  # Format: YYYYMMDDHHMMSS
  random_part = ''.join(random.choices(string.ascii_letters + string.digits, k=length))  # 8 random characters
  return f"{date_string}-{random_part}"




# Read a JSON file
#
# filePath. string. required.
# The path to the file
#
# errorMode. int. optional. default is 0.
# If 0, then this will print whatever went wrong
# in the event of an error.
# If 1, then this will return the error message
# If 2, then this will raise a new Exception.
#
# previousData. object. optional. default is None.
# For idempotence, you can pass in the results of a previous
# run of this function. If this function returned something 
# previously, then it will just return that previous data 
# instead of reading the file again.
#
#
def readJSON(filePath, errorMode=0, previousData=None):
  dataObj = None
  errorMsg = None

  try:

    if(not previousData):

      if(path.isfile(filePath)):
        with open(filePath) as jsonFile:

          jsonFileContents = jsonFile.read()

          if(len(jsonFileContents) == 0 or re.match(r'^\s+$', jsonFileContents)):
            raise Exception(f"The file {filePath} is empty or malformed")
          else:
            dataObj = json.loads(jsonFileContents) 
            jsonFile.close() 

      else:
        raise Exception(f"No file at: {filePath}")
    
    else:
      dataObj = previousData

    if(dataObj == None):
      raise Exception(f"The file {filePath} is empty or malformed")
  
  except Exception as e:
    if(errorMode == 0):
      print(f"Error: {str(e)}")
    else:
      errorMsg = str(e)
  
  finally:

    #Handle the output and the errors
    if(errorMode == 0):
      return dataObj
    elif(errorMode == 1):
      return (dataObj, errorMsg)
    elif(errorMode == 2):
      if(errorMsg != None):
        raise Exception(errorMsg)
      else:
        return dataObj
      


# def normWindowsPath(dirtyURI, asObj=False):
#   purePath = PureWindowsPath(path.normpath(dirtyURI))
#   return purePath if asObj else str(purePath)

