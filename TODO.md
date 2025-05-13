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

## 8 DONE
Need to redo the init thing so that it's -init "handle-name-here" then you fill in the settings, then it's -configure without the name of the settings.

## 9 N/A
Need to be able to overwrite or append new secrets in a batch.

## 10
Need a utility called Paths which give us all of the paths that this thing uses, and that will be broken out of the Configure.py utility. 

## 11
Need to rename the Init.py InitStage1.py

## 12 
Need to use the runModuleInVenv instead of activate with all of the different arguments.

## 13
Need to figure out how to upgrade easily.
The current version will be in one of the files. 
There's going to be an upgrade script which will: 

Read the version to see if its compatible with the newest version.
Take a backup of the main.json file from the launcher and store it in the data folder. 
Store the version of the current one in a text file and put it in the data folder.
Pull a copy of the python_launchpad from github. Configure it.
The update script will also have a revert method that will restore the old version of the launchpad, which was stored in the data folder.

## 14 DONE.
Need to change Background.py Foreground.py to Task.py and Monitor.py

## 15. 
We need to have a command:

-add-meta-field -public-field -field-title "My Title Here" -field-data "Stuff goes here" -for-key MY_SECRET

So that we can display metadata. The public-field flag means that the metadata is safe for the public to see. Otherwise it will be encrypted

## 15
Need to format the error when there's a syntax error on the Task or Monitor.py file.


## 16 DONE. Put this in the TaskRunner.
For stacktrace, figure out where to put this:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
    error_string = ''.join(lines)
    print(error_string)

## 17 
Need to have some way to reset all of the thread-safe variables.

## 18 
See def printMsg():

## 19
getVar, getSecret- these should be the same thing. getSecret is currently not thread-safe, so I should make it threadsafe. Maybe instead of a secrets.json file, it should be a directory and each secret should have its own file keyes to the name of the secret.

## 20 DONE
Need easy way to list secrets. Need a -list-secrets call.

## 21
Need to be able to launch subtasks. 

## 22 DONE
secrets.json needs to be broken out into its own directory and each secret is a file. This way it can also be 
used in the getVar setVar, and the secrets can be version controlled. Also, the public-key should be in that folder
so that it can also be version-controlled.



## Troubleshooting:
If, upon -init, you get this error:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 517: character maps to <undefined>
It's because a microsoft smart quote has made it's way into the sourcecode.




## Windows Credential Manager

You'll see the private key in Windows Credential Manager in <my proj>_launchpad