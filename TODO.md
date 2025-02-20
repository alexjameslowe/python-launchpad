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
