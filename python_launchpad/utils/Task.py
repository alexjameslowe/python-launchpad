
from python_launchpad.utils import Constants as C
from python_launchpad.utils.VEnv import activate
from python_launchpad.utils.Var import getVar

###################################################################
##
##  A wrapper around the task so that we can have a nice oop way 
##  of dealing with tasks when it comes to composite tasks
##
##  Author Alex Lowe
##
###################################################################


class Task:

  def __init__(self, taskInfo):
    self.taskInfo = taskInfo.info

 
  def run(self, args=None, mode=C.TASK_RUN_COMPOSITE, quietException=False):
    taskInfo = self.taskInfo

    if(mode == C.TASK_RUN_BACKGROUND):
      activate(taskInfo, args=args, background=True)
    
    elif(mode == C.TASK_RUN_FOREGROUND):
      activate(taskInfo, args=args, foreground=True)

    elif(mode == C.TASK_RUN_COMPOSITE):
      activate(taskInfo, args=args, foreground=True)

    else:
      raise Exception(f'Unknown run mode {mode}')

    if(getVar('ERROR', None) != None):
      if(not quietException):
        raise Exception(f"Error in {taskInfo['taskName']}. Check the {taskInfo['taskName']}.txt file for details.")
      return False 
    
    return True

  