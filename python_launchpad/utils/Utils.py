import sys
from os import path
import json
import re
import traceback
from pathlib import PureWindowsPath
from datetime import datetime, timedelta

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
sys.path.append(path.dirname(SCRIPT_DIR))


def formatStacktrace():
  parts = ["Traceback (most recent call last):\n"]
  parts.extend(traceback.format_stack(limit=25)[:-2])
  parts.extend(traceback.format_exception(*sys.exc_info())[1:])
  return "".join(parts)



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
      

def validateSettingsInfo(info):
  pass


def normWindowsPath(dirtyURI, asObj=False):
  purePath = PureWindowsPath(path.normpath(dirtyURI))
  return purePath if asObj else str(purePath)


# Calculate the qb report bounds as well as the calpers report bounds
# based on a single date.
#
#
def getQBAndCalpersBounds(testDateString):

  # 1  2  3  4  5  6  7  8  9  10 11 12 13 14

  # 04 05 06 07 08 09 10 11 12 13 14 15 15 17  QB Period 1

  # 18 19 20 21 22 23 24 25 26 27 28 29 30 31  QB Period 2


  # 1  2  3  4  5  6  7  8  9  10 11 12 13 14

  # 28 29 30 01 02 03 04 05 06 07 08 09 10 11  Calpers Period

  try:
    testDate = datetime.strptime(testDateString, "%Y-%m-%d")

    if(testDate == None):
      raise Exception("No date found. 593829")

    northStar = datetime.strptime('2024-05-17', "%Y-%m-%d")
    northStarM13 = northStar - timedelta(13)

    qbPeriodStart = None 
    qbPeriodEnd = None
    calpersPeriodStart = None 
    calpersPeriodEnd = None

    if(testDate > northStarM13):

      keepGoing = True
      ratchet = northStar 

      while(keepGoing):

        # If the test date is in the future 
        #
        #                                     North Star  
        #                                          V
        #  2022-xx-xx ----------------------- 2022-xx-yy           
        #                                                              2024-05-12
        #                                                                   ^
        #                                                           Test date out here in the future 
        #
        #  or
        #
        #                                     North Star  
        #                                          V
        #  2022-xx-xx ----------------------- 2022-xx-yy     
        #                     ^
        #                  Test date
        #                                
        #
        #  Then do this:
        #  Start adding up 14 to the north star date until the north star
        #  is finally greater or equal to the test date.
        #
        #                                       ratchet
        #                                          V
        #  2024-05-04 ----------------------- 2024-05-17 
        #                      ^
        #                 2024-05-12
        #                 Test Date
        # 
        if(ratchet >= testDate):
          qbPeriodEnd = ratchet 
          qbPeriodStart = ratchet - timedelta(13)
          
          calpersPeriodEnd = qbPeriodEnd - timedelta(6)
          calpersPeriodStart = calpersPeriodEnd - timedelta(13)

          keepGoing = False
          break

        ratchet += timedelta(14)

    else:

      keepGoing = True
      ratchet = northStarM13

      while(keepGoing):

        # 
        #                            North Star - 13 days                North Star
        #                                  V                                 V
        #                             2024-xx-xx ----------------------- 2024-xx-yy 
        #               ^
        #           2022-04-02
        #           Test Date
        #
        #  Then do this:
        #  Start subtracting 14 to the northStarM13 until the northStarM13
        #  is finally less than or equal to the test date.
        #
        #   ratchet
        #      V
        #  2024-05-04 ----------------------- 2024-05-17 
        #                      ^
        #                 2024-05-12
        #                 Test Date
        # 
        if(ratchet <= testDate):
          qbPeriodStart = ratchet 
          qbPeriodEnd = ratchet + timedelta(13)
          
          calpersPeriodEnd = qbPeriodEnd - timedelta(6)
          calpersPeriodStart = calpersPeriodEnd - timedelta(13)

          keepGoing = False
          break

        ratchet -= timedelta(14)
        
    return qbPeriodStart, qbPeriodEnd, calpersPeriodStart, calpersPeriodEnd

  except Exception as e:
    print(f"getQBAndCalpersBounds: {str(e)}")
    formatStacktrace()

    return None, None, None, None

  