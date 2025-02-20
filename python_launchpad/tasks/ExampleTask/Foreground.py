import sys
import os
import sys
from rich.live import Live
from rich.table import Table
from python_launchpad.utils.Configure import getMainSetting, getDataDirectory, getLaunchpadDirectory
from python_launchpad.utils.Format import joinPath
from time import sleep

# import warnings. This is for an error that can happen with pandas.
# warnings.simplefilter(action = "ignore", category = RuntimeWarning)


#https://stackoverflow.com/questions/16981921/relative-imports-in-python-3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from python_launchpad.utils.Var import setVar, rmVar, getVar, RUNNING, PROCESS, GRACEFUL_EXIT
  

#Run the report on a background processes, and gather information about what's going
#on to the user to update the screen as we go.
def monitor():

  #This is keeps the loop going, and its set to false
  #when the subprocess running the report stops
  keepGoing = True 

  #create the table
  table = Table(min_width=500)
  table.add_column("TITLE GOES HERE", style='on green')  

  testInt = 0

  #start the live updating context for the report
  with Live(table, refresh_per_second=4) as live:
    
    #The settings are ok, the subprocess started ok, so 
    #every 2 seconds we're going to check in with the 
    #subprocess and see what's going on. Log out the 
    #cross-process variables and update the table.
    #could get really fancy with this but this is a good start.
    while(keepGoing):

      sleep(1)

      testInt += 1

      table = Table(min_width=500)
      table.add_column("ALEX TITLE GOES HERE")
      table.add_row(f' Running report for: ALEX SOMETHING GOES HERE', style="on blue")
      if(getVar(RUNNING, asbool=True)):
        table.add_row(f' (background process = {str(getVar(PROCESS, defval=0))})', style="on blue")
        table.add_row('')

      if(not getVar(RUNNING, asbool=True)):
        keepGoing = False
        table.add_row(" Finished Running!", style="on blue")
        #table.add_row(" Look for long-log.txt For details on this run of the program")
      
      else:
        table.add_row(" Running...", style="on blue")

      table.add_row('')
      table.add_row(f' test-int: {str(testInt)}', style="on red")

      if(getVar(GRACEFUL_EXIT, asbool=True)):
        table.add_row(f' gracefully exited', style="on green")
      # table.add_row('')
      # table.add_row(f' # Days Skipped: {str(getVar(DAYS_SKIPPED, defval=0))}')
      # table.add_row('')
      # table.add_row(f' # File Errors: {str(getVar(FILE_ERRS, defval=0))}')
      # table.add_row('')
      # table.add_row(f' # Unknown Errors: {str(getVar(UNKNOWN_ERRS, defval=0))}')
      # table.add_row('')
      # table.add_row(' Directories Created:')
      # table.add_row(getDirectoriesVarForReport())

      live.update(table)


  
