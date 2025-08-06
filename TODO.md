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

$ python
>>> import keyring
>>> keyring.get_keyring()
<keyring.backends.SecretService.Keyring object at 0x7f9b9c971ba8>
>>> keyring.set_password("system", "username", "password")
>>> keyring.get_password("system", "username")
'password'

## Troubleshooting:
If, upon -init, you get this error:
UnicodeDecodeError: 'charmap' codec can't decode byte 0x9d in position 517: character maps to <undefined>
It's because a microsoft smart quote has made it's way into the sourcecode.





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




## Windows Credential Manager

You'll see the private key in Windows Credential Manager in <my proj>_launchpad