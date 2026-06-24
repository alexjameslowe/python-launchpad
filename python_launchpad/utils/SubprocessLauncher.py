from os import path
from sys import path as syspath, exc_info
import subprocess
from time import sleep
import json
import traceback
from datetime import datetime


from python_launchpad.utils.Configure import getDataDirectory, getPythonExecutable
from python_launchpad.utils.Format import joinPath, dashCaseToFlagCase

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, getVar, ERROR, RUNNING, PROCESS, GRACEFUL_EXIT
  
class ValidationException(Exception):
  pass


#Run the report on a background processes, and gather information about what's going
#on to the user to update the screen as we go.
def launch(args, taskInfo):
  
  #TODO remove this
  #Set this to false to start with
  #setVar(GRACEFUL_EXIT, False)

  #We're going to record the process
  pid = 0

  retainHistory = taskInfo.get('retainHistory', False)

  outputFile = joinPath(getDataDirectory(), f"{taskInfo.get('taskName', None)}_output.txt")
  errorFile = joinPath(getDataDirectory(), f"{taskInfo.get('taskName', None)}_error.txt")

  try:

    fileMode = "a" if retainHistory else "w+"
    now = datetime.now()
    dateStr = now.strftime("%Y-%m-%d %H:%M:%S")
    openingString =  f"{taskInfo['taskName']}: {dateStr}{ ' (retaining history)' if retainHistory else '' }"

    #Clear out the output and error files
    with open(outputFile, fileMode) as output, open(errorFile, fileMode) as error:
      output.write("\r\n")
      output.write("\r\n")

      output.write("*****************************************")
      output.write("\r\n")
      output.write(f"OUTPUT: {openingString}")
      output.write("\r\n")

      error.write("*****************************************")
      error.write("\r\n")
      error.write(f"ERROR: {openingString}")
      error.write("\r\n")


    # #TODO make this work with linux  
    # #ALEX-20250304
    # setVar(RUNNING, True)  
   
    #Put together arguments for the subprocess. Note that we're calling
    #the python executable from the virtual environment if a virtual environment
    #is specified. otherwise we're just going to use the system python_handle
    subProcessArgs = [
      getPythonExecutable(),
      joinPath(SCRIPT_DIR, '..', 'main.py'),
    ]

    taskArg = taskInfo.get('taskArg', None)
    if(taskArg == None):
      raise Exception('Missing task argument')
    
    subProcessArgs.append(dashCaseToFlagCase(taskArg))

    otherArgs = taskInfo.get('args', None)

    argsKVP = {}
    fullValidator = taskInfo.get('validator', None)

    #If the task has other arguments that it's expecting, 
    #we're going to loop through the task-info and make sure that those
    #arguments get appended to the subprocess just how they came in through the arguments.
    if(otherArgs != None):
      for otherArg in otherArgs:
        argName = otherArg.get('name', None)

        if(argName == None):
          raise Exception("In the TaskInfo, and argument is missing the name field.")

        argValue = args.get(argName, None)
        argNameFlagCase = dashCaseToFlagCase(argName)

        isFlag = otherArg.get('flag', False)

        #If it's a flag without any value, then just append the flag-case name of the arg
        if(isFlag and argValue == "1"):
          subProcessArgs.append(argNameFlagCase)

        #Else, if it's an argument that has to come with some kind of value, then we're
        #going to append both it and the value if the value is non-None.
        elif(isFlag == False and argValue != None):

          validator = otherArg.get('validator', None) 
          valType = otherArg.get('type','str')
          originalArgVal = argValue

          if(valType == 'int'):
            argValue = int(argValue) 
          elif(valType == 'float'):
            argValue = float(argValue) 
          elif(valType == 'json'):
            argValue = json.loads(argValue)
          elif(valType == 'yyyy-mm-dd'):
            argValue = datetime.strptime(argValue, "%Y-%m-%d")

          validationErr = validator(argValue)  if validator != None else None
          if(validationErr != None):
            raise Exception(f'Validation error: {argNameFlagCase}: {validationErr}')

          argsKVP[argName] = argValue

          #Reset this to a string. the argsKVP will have the full date objec for the validator
          #But for the subprocess launcher we need to to be a string.
          if(valType == 'yyyy-mm-dd'):
            argValue = originalArgVal

          subProcessArgs.append(argNameFlagCase)
          #have to convert to string or else you're going to get complaints 
          #when you concatenate the args into a command and run it.
          subProcessArgs.append(str(argValue))

    #If there's a validator attached to the info itself, then send it
    #ALL the arguments, and it will be able to do things like check to see
    #if start_date is before end_date and things like that.
    if(fullValidator):
      validationErr = None
      try:
        errMsg = fullValidator(argsKVP)
        if(errMsg):
          validationErr = errMsg
      except Exception as e:
        validationErr = f'Validator function encountered an error: {str(e)}'

      if(validationErr != None):
        raise ValidationException(validationErr)


    # And then add this one in so that it knows that it's the background task
    # and it therefore it will actually do the report.
    subProcessArgs.append('-background')

    #Call the subprocess. In the past I've gone down rabbit holes with trying to do 
    #this on a daemon thread, but this always ends up being more straightforward.
    with open(outputFile, "a") as output, open(errorFile, "a") as error:
      process = subprocess.Popen(subProcessArgs, stdout=output, stderr=error)
      pid = process.pid

  except ValidationException as e:
    print(f'Validation Error: {str(e)}')

    return False

  except Exception as e:
    print(f'Error starting Task: {str(e)}')

    exc_type, exc_value, exc_traceback = exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    error_string = ''.join(lines)
    print(error_string)
   
    return False

  setVar(PROCESS, str(pid))
  sleep(2)
  
  return True
