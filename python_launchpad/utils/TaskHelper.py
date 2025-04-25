############################################################################
#
#  Utility for coordinating with the tasks to provide argument parsing and 
#  information about the task that has to run.
#
#  Author Alex Lowe
#
############################################################################

from python_launchpad.utils.Format import dashCaseToFlagCase

import sys


#Help the main.py parse out the cli arguments according to the demands of the different tasks.
def parseArgs(parser, tasks):

  taskInfoOfCurrentTask = None

  #Loop through the tasks and find the one that's running
  for info in tasks: 

    taskName = info.get('taskName', None)
    taskArg = info.get('taskArg', None)
    otherArgs = info.get('args', None)  

    if(taskName == None):
      raise Exception('No taskName was present. I need you to tell me what the taskName is, and this has to match with a directory of that same name in the tasks directory. See the documentation for details.')

    if(taskArg == None):
      raise Exception(f"No taskArg was present for task {taskName}. Without this, I can't tell what task you want me to run from the command-line arguments. I'm happy to do your tasks, but I can't read your mind!")

    taskArgFlag = dashCaseToFlagCase(taskArg)

    if(taskArgFlag in sys.argv):
      taskInfoOfCurrentTask = info
      break

  # if(taskInfoOfCurrentTask == None):
  #   raise Exception("I couldnt find a task to match the arguments.")

  #The idea is that we only add in the arguments of the task that we're running.
  #So if there's any task that's supposed to run, go through and add all the arguments.
  if(taskInfoOfCurrentTask):

    #Now take the task and we're going to parse the arguments.
    info = taskInfoOfCurrentTask
    taskName = info.get('taskName', None)
    taskArg = info.get('taskArg', None)
    otherArgs = info.get('args', None)  

    #Add in the main task argument that the program will use tell what task to launch.
    parser.add_argument(dashCaseToFlagCase(taskArg), help=f'Run the {taskName} task.', required=False, default="0", const="1", nargs='?')

    #Any other arugments that are present for the task, add them in as well. 
    if(otherArgs != None):

      for otherArg in otherArgs: 

        otherArgName = otherArg.get('name', None)
        if(otherArgName == None):
          raise Exception(f"There's an argument in the task {taskName} that does not have a name") 

        if(otherArg.get('flag', False) == False):
          parser.add_argument(dashCaseToFlagCase(otherArg.get('name', None)), help=otherArg.get('help',None), required=False, default=otherArg.get('default',None), const=otherArg.get('const',None), nargs=otherArg.get('nargs',None))
        else:
          parser.add_argument(dashCaseToFlagCase(otherArg.get('name', None)), help=otherArg.get('help',None), required=False, default="0", const="1", nargs='?')



# Loop through the tasks and see if any of them can take a crack at this command.
#
def getTaskInfo(args, tasks):
  for info in tasks: 

    taskName = info.get('taskName', None)
    taskArg = info.get('taskArg', None)

    if(taskName == None):
      raise Exception('No taskName was present. I need you to tell me what the taskName is, and this has to match with a directory of that same name in the tasks directory. See the documentation for details.')

    if(taskArg == None):
      raise Exception(f"No taskArg was present for task {taskName}. Without this, I can't tell what task you want me to run from the command-line arguments. I'm happy to do your tasks, but I can't read your mind!")


    if(args.get(taskArg,None) == "1"): 
      return info
  
  return None


  

