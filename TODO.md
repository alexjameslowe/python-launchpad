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


## Troubleshooting:
If, upon -init, you get this error:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 517: character maps to <undefined>
It's because a microsoft smart quote has made it's way into the sourcecode.



Traceback (most recent call last):
  File "./windu.py", line 4, in <module>
    main()
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\main.py", line 85, in main
    module = runModuleInVEnv('windu_launchpad.utils.InitStage2')
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\utils\VEnv.py", line 288, in runModuleInVEnv
    wasVenvCreated = createVEnv()
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\utils\VEnv.py", line 127, in createVEnv
    venvPath = getVenvPath()
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\utils\VEnv.py", line 116, in getVenvPath
    dataDirectory = getDataDirectory()
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\utils\Configure.py", line 113, in getDataDirectory
    launchHandle = getMainSetting("launchpad_handle")
  File "C:\Users\AlexLowe\Documents\ICS_all\ltest\windu_launchpad\utils\Configure.py", line 85, in getMainSetting
    raise Exception(f"No setting for '{key}'. Did you run with the -config flag yet?")
Exception: No setting for 'launchpad_handle'. Did you run with the -config flag yet?
PS C:\Users\AlexLowe\Documents\ICS_all\ltest>