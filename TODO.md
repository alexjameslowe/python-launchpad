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

## 11 DONE
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

## 17 DONE
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

## 23 
There's some places where we're concatenating string for system commands e.g. pip install and we're wrapping uris with quotes. We should make sure that the quotes that the uris contain are escaped.

## 24
It should make a gitignore if there isn't one and add,
__pycache__
optibus_data
optibus_launchpad
Or else if there is one, then in the initalization it should say "hey add these to your gitignore"

## 25
There should be an easy way to pull down a project from git and get it going with a copy of the python_launchpad. main.py -existing the-cool-project and it takes care of everything.

## 26 
Possible switch to MODE_EAX instead of MODE_CBC
AI Overview
Learn more
In most modern applications, MODE_EAX is generally considered better than MODE_CBC due to its built-in authentication and integrity checks. While CBC (Cipher Block Chaining) is a widely used block cipher mode, EAX (Galois/Counter Mode) provides both confidentiality and data integrity, making it more secure in scenarios where data authentication is crucial. 
Here's a more detailed comparison:
MODE_EAX (Galois/Counter Mode): 

## 27 
There should be an error file separate from the output file.
If there's an error in the error file after the run is finished, then it should display the error on the monitor, and have a hook to handle it, like with an email transport or something.

Ok I did that, but all of the errors are going to the output file.

This part in VEnv.py:

    except ModuleNotFoundError as err:
      handleException()
      print(f"Module not found: (4746383) {str(err)} {tasksModuleName} {taskName}")
    except Exception as err:
      handleException()
      print(f"Task error: (563290) {str(err)}")

What should happen is that on error it should examine the 


## 28
Figure out how to get a headless backend working for server environments
https://pypi.org/project/keyring/

docker run -it -d --privileged ubuntu:18.04

$ apt-get update
$ apt install -y gnome-keyring python3-venv python3-dev
$ python3 -m venv venv
$ source venv/bin/activate # source a virtual environment to avoid polluting your system
$ pip3 install --upgrade pip
$ pip3 install keyring
$ dbus-run-session -- sh # this will drop you into a new D-bus shell
$ echo 'somecredstorepass' | gnome-keyring-daemon --unlock # unlock the system's keyring

```bash
>>> import keyring
>>> keyring.get_keyring()
<keyring.backends.SecretService.Keyring object at 0x7f9b9c971ba8>
>>> keyring.set_password("system", "username", "password")
>>> keyring.get_password("system", "username")
'password'
```

## 29
Typing of arguments is a mess.
If you define the default value of a variable, then the type coming out of the args kvp should be the same type. Dates should be dates, ints should be ints etc. If you need to raw string value, then there should be an entry in the args kvp "*_raw" e.g. if it's my date, then args['mydate'] will be a date, but args['mydate_raw'] will be the string in yyyymmdd form.

## 30
We really need to split the code up between code that runs "normally" and code that's supposed to run in the venv. 

## 31 
Need to pull together the keyring stuff a bit better. The secret files shouldn't have this __aes thing. The names of the files should just be all goobeldygook. The manifest will keep it all straight, and it's __aes thing will just be that the file is internally delimited that way, with some delimiter string to separate the aes and non-aes parts.

## 34
Need to have docker backend where will will create images instead of venvs. I say that after dealing with this damn cffi problem for a long time today.

## 35
The upgrade has to work in WSL2

## 36
Ok so deployment is... it's just awful. I just spend an hour trying to do it and it was just terrible. Also, this business with THREE json files. No... That's just terrible. Also, I found that I had to explicitly set the "keyring_backend" to false on the main.json file for the ubuntu settings or else it wants to use the backend which of course will fail because I don't know how to do that yet.

## 37
Tried an argument 'test' and it complained. 'testrun' worked fine. So test is reserved and it should complain.

## 38
It didn't show an error when I had paramiko in the task but i didn't actually include it. The error showed up in the output. Figure that out. Errors should always get reported to the client

## 39
It should be able to respond gracefully to a keyboard interrupt and reset the variables and everything.

## 40
This
  'args': [
      
    {
      'name':'testrun',
      'help':'This is a test-run of the script',
      'flag':True
    },
The flag is always being reported as 1. This isn't right. flag should just be boolean and it should be super easy to get that from the args

## 41 
Needs to support keyboard-interrupt and it should definitely wipe the variables when its done

## 42
set-private-key need to make sure that the path that you put in here can be relative to the cwd, or absolute.


## 43 
Incorporate this 

def is_time_between(now, start, end):
    if start <= end:
        return start <= now <= end
    else:
        # crosses midnight
        return now >= start or now <= end

## Troubleshooting:
If, upon -init, you get this error:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 517: character maps to <undefined>
It's because a microsoft smart quote has made it's way into the sourcecode.

## 44
We need some kind of a thing where we know what arguments are printable and which are sensitive. 
there needs to be some kind of a filter so that you're never accessing task arguments directly, there's a helper object that's doing that.
When you print, it would internally switch to a mode where the helper object switches to a mode where it will redact the sensitive cli arguments. This is so that we can safely retain logs of past runs without worrying about unsafe arguments getting passed.




```python
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import os

def encrypt_png(key, filename):
    chunk_size = 64 * 1024
    output_filename = filename + ".enc"
    file_size = os.path.getsize(filename)
    iv = get_random_bytes(16)

    cipher = AES.new(key, AES.MODE_CBC, iv)

    with open(filename, 'rb') as infile:
        with open(output_filename, 'wb') as outfile:
            outfile.write(file_size.to_bytes(16, 'big'))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunk_size)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(cipher.encrypt(chunk))
    print(f"Encrypted file saved as: {output_filename}")

# Example Usage
key = b'Sixteen byte key'  # Key should be 16, 24, or 32 bytes long
filename = "image.png"

encrypt_png(key, filename)
```

## 45
We need a setup-linux.py setup-windows.py script that you can copy and it will just set everything up for you: Pull down a copy of the master branch, get the name of your launchpad, initialize it etc, gracefully complain if git isn't installed, complain if requrests isn't installed.

## 46
C:\Users\...\AppData\Local\Microsoft\WindowsApps\PythonSoftwareFoundation.Python.3.9_qbz5n2kfra8p0\python.exe: No module named virtualenv

If we don't have virtualenv installed, then we need to catch this error better.


## 47 
When we have a bad installation, it will often give us this:

ERROR: Could not find a version that satisfies the requirement requests==2.34.2 (from -r /mnt/c/ICS/ICS/heartbeat/heartbeat_data/linux_wsl2_requirements.txt (line 3)) (from versions: 0.2.0, 0.2.1, 0.2.2, 0.2.3, 0.2.4, 0.3.0, 0.3.1, 0.3.2, 0.3.3, 0.3.4, 0.4.0, 0.4.1, 0.5.0, 0.5.1, 0.6.0, 0.6.1, 0.6.2, 0.6.3, 0.6.4, 0.6.5, 0.6.6, 0.7.0, 0.7.1, 0.7.2, 0.7.3, 0.7.4, 0.7.5, 0.7.6, 0.8.0, 0.8.1, 0.8.2, 0.8.3, 0.8.4, 0.8.5, 0.8.6, 0.8.7, 0.8.8, 0.8.9, 0.9.0, 0.9.1, 0.9.2, 0.9.3, 0.10.0, 0.10.1, 0.10.2, 0.10.3, 0.10.4, 0.10.6, 0.10.7, 0.10.8, 0.11.1, 0.11.2, 0.12.0, 0.12.1, 0.13.0, 0.13.1, 0.13.2, 0.13.3, 0.13.4, 0.13.5, 0.13.6, 0.13.7, 0.13.8, 0.13.9, 0.14.0, 0.14.1, 0.14.2, 1.0.0, 1.0.1, 1.0.2, 1.0.3, 1.0.4, 1.1.0, 1.2.0, 1.2.1, 1.2.2, 1.2.3, 2.0.0, 2.0.1, 2.1.0, 2.2.0, 2.2.1, 2.3.0, 2.4.0, 2.4.1, 2.4.2, 2.4.3, 2.5.0, 2.5.1, 2.5.2, 2.5.3, 2.6.0, 2.6.1, 2.6.2, 2.7.0, 2.8.0, 2.8.1, 2.9.0, 2.9.1, 2.9.2, 2.10.0, 2.11.0, 2.11.1, 2.12.0, 2.12.1, 2.12.2, 2.12.3, 2.12.4, 2.12.5, 2.13.0, 2.14.0, 2.14.1, 2.14.2, 2.15.1, 2.16.0, 2.16.1, 2.16.2, 2.16.3, 2.16.4, 2.16.5, 2.17.0, 2.17.1, 2.17.2, 2.17.3, 2.18.0, 2.18.1, 2.18.2, 2.18.3, 2.18.4, 2.19.0, 2.19.1, 2.20.0, 2.20.1, 2.21.0, 2.22.0, 2.23.0, 2.24.0, 2.25.0, 2.25.1, 2.26.0, 2.27.0, 2.27.1, 2.28.0, 2.28.1, 2.28.2, 2.29.0, 2.30.0, 2.31.0, 2.32.0, 2.32.1, 2.32.2, 2.32.3, 2.32.4, 2.32.5)
ERROR: No matching distribution found for requests==2.34.2 (from -r /mnt/c/ICS/ICS/heartbeat/heartbeat_data/linux_wsl2_requirements.txt (line 3))

And what we should do is have a nice complaint to the user that will show this list.



## 48

When i ran configure in WSL2 I had keyring set to true in the main.json

it gave me this error
Error: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.

What it didn't tell me was that it never generated the damn public_key.txt and so i had to chase that down for an hour. So that should be much more graceful.

## 49 

Ran into this error on launch:
Monitor error: (119384) [Errno 2] No such file or directory
/blah/blah/heartbeat/heartbeat_data/vars/__RUNNING.txt