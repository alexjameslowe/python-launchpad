## 1 DONE

## 2
make this work for linux, with the lenv

      #TODO make this work for linux, with the lenv
      #(joinPath(projectDirectory, venv, 'Scripts', 'python.exe') if venv != None else pythonHandle),
      joinPath(projectDirectory, 'wenv', 'Scripts', 'python.exe'),

## 3 
TODO make the Var work for linux.
Also, vars should be moved to the users profile folder, because they should be based on the user. Now that I think of it, they should also be based on the task as well.

## 4
Make the setup.py file and figure out the distribution

## 5
Our portalocker solution in Var should maybe be this instead:
https://docs.python.org/3/library/multiprocessing.shared_memory.html



## 6
See in Configure.py

      #
      # #If the key is the hopper directory, then we're going to make sure
      # #that it exists.
      # if(key == "output_dir"):
      #   outputDirURI = rf"{value}" #For windows slashes
      #   if(not path.isdir(outputDirURI)):
      #     mkdir(outputDirURI)

The user should have a function in Info.py which will take the old settings and the new settings and the user can then decide what to do when the settings change from that function, e.g. makeing new directories and whatnot.


## 7
There should be a command that will reset the initialization name, that way if you don't like it you can do something else.

## 8
Need to redo the init thing so that it's -init "handle-name-here" then you fill in the settings, then it's -configure without the name of the settings.

## 9
Need to be able to overwrite or append new secrets in a batch.

## 10
Need a utility called Paths which give us all of the paths that this thing uses, and that will be broken out of the Configure.py utility. 

## 11
Need to rename the Init.py InitStage1.py

## 12 
Need to use the runModuleInVenv instead of activate with all of the different arguments.

## 13
Need to figure out how to upgrade easily.

## 14
Need to change Background.py Foreground.py to Task.py and Monitor.py


## 15
Need to format the error when there's a syntax error on the Background or Foreground.py file.

## 16
For stacktrace, figure out where to put this:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    error_string = ''.join(lines)
    print(error_string)


## Troubleshooting:
If, upon -init, you get this error:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 517: character maps to <undefined>
It's because a microsoft smart quote has made it's way into the sourcecode.




## Windows Credential Manager

You'll see the private key in Windows Credential Manager in <my proj>_launchpad