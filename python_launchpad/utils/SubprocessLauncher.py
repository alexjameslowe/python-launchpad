from os import path
from sys import path as syspath
import subprocess
from time import sleep

from python_launchpad.utils.Configure import getDataDirectory, getPythonExecutable
from python_launchpad.utils.Format import joinPath, dashCaseToFlagCase

#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = path.dirname(path.abspath(__file__))
syspath.append(path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, getVar, RUNNING, PROCESS, GRACEFUL_EXIT
  

#Run the report on a background processes, and gather information about what's going
#on to the user to update the screen as we go.
def launch(args, taskInfo):
  
  #Set this to false to start with
  setVar(GRACEFUL_EXIT, False)

  #We're going to record the process
  pid = 0

  outputFile = joinPath(getDataDirectory(), f"{taskInfo.get('taskName', None)}.txt")

  try:

    #Clear out the output file.
    with open(outputFile, "w+") as f:
      f.write("")

    isRunning = getVar(RUNNING, asbool=True)
    if(isRunning):
      raise Exception("There's already a report running. Please wait for it to stop.")

    #TODO make this work with linux    
   
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
          subProcessArgs.append(argNameFlagCase)
          subProcessArgs.append(argValue)


      
    # See, we're automating this:
    # subProcessArgs.append('-start-date')
    # subProcessArgs.append(args.start_date)
    # subProcessArgs.append('-end-date')
    # subProcessArgs.append(args.end_date)

    # And then add this one in so that it knows that it's the background task
    # and it therefore it will actually do the report.
    subProcessArgs.append('-background')

    #Call the subprocess. In the past I've gone down rabbit holes with trying to do 
    #this on a daemon thread, but this always ends up being more straightforward.
    with open(outputFile, "w") as f:
      process = subprocess.Popen(subProcessArgs, stdout=f)
      pid = process.pid

  except Exception as e:
    print(f'Error starting report: {str(e)}')
    return False

  setVar(PROCESS, str(pid))
  sleep(2)
  
  return True
