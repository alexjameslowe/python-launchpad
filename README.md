
# Python Launchpad
The purpose of this library is to provide a base from which you can write a program that does four important things right out of the box that are a real headache to set up each time you want a new python tool:

## 1.
Launches a background subprocess which completes a long-running process and shows a report table to the user as its working

## 2. 
Provides you with a way to monitor a process, as define thread-safe variables that can be set and get by both the task and the monitor.

## 3. 
Manages virutal-environments behind the scenes. It will install them and activate them behind the scenes so that you don't have to do that. You just run the commands from your system python >= 3.5 and the meat of the program will be run in a virtual environment that you don't have to set up yourself.

## 4.
Allows multiple configurations for multiple platforms, e.g. Linux, Windows, WSL2.


## Installation

### Note for Windows WSL2 users:
#### Python usually lives in /mnt/c/Program Files and if you're running the installation commands from an Ubuntu shell, you're probably going to get an error "Permission Denied" when it attempts to create the virtual environmnet. You can either make things easy on yourself and just run the installation commands in Powershell, or you can specify a python version location that your Ubuntu shell has permissions for.

1. Copy python_launchpad from the source into your project folder.

2. cd to your project folder.

3. Make sure that the following entries are in your gitignore:

python_launchpad/
<project-name-here>_settings.json
<project-name-here>_data

<project-name-here> is a standin for a project handle that you decide. Python Launchpad will add some files to your project directory and this handle is a convenience so that you can easily distinguish launchpad files from other things in your directory. E.g., there will be a "coolproject_info.py", "coolproject_tasks.py" etc.

```powershell
python3 .\python-launchpad\main.py -init coolproject
```

You'll notice that some files appear, among them coolproject_settings.json.

Open this file up. It will look like this:

```json
{
  "launchpad_handle":"python_launchpad",
  "windows": {
    "windows": {
      "system_python_handle":"python3",
      "python_location_for_venv":"C:/Program Files/Python310",
      "keyring_backend":true
    }
  },
  "linux": {
    "wsl2": {
      "system_python_handle":"python3",
      "python_location_for_venv":"/mnt/c/Program Files/Python310",
      "keyring_backend":true
    }, 
    "ubuntu": {
      "system_python_handle":"python3",
      "python_location_for_venv":"/python310/location/goes/here",
      "keyring_backend":false
    }
  },
  "mac": {
    "mac": {
      "system_python_handle":"python3",
      "python_location_for_venv":"/python310/location/goes/here",
      "keyring_backend":false
    }
  }
}
```

1. *launchpad_handle:* The launchpad handle, e.g. "my-proj". The name of the project. This will be reflected in the names of the main entrypoint and the names of all other files that get generated.

2. *system_python_handle:* This is the alias of python that your CLI session uses by default. Often this is "python" or "python3"

3. *python_location_for_venv:* Python Launchpad will handle the virtual environment and keep it out of the way. In this field you'll specify which version of python you want the virtual environment to use.

4. *keyring_backend:* Some environments have a suitable backend that the python keyring library can communicate with. (See https://pypi.org/project/keyring/ for details) Setting up a usable backend on a headless linux server is really annoying however, so we have the option to just set this to false and it will use the data folder to store the private key. Servers typically have private keys anyway so this isn't too big of a deal, although it does add extreme primacy to including the data folder in your gitignore. The last thing you want is a private key making it into the repository.

Now, from your CLI, run the following command:

```powershell
python3 coolproject.py -config
```

It will configure your program. You can delete the coolproject_settings.json afterward. Note that the virtual enviornment will start building. It will also generate a public and private key for secrets. Wait until its finished.

Make sure your .gitignore contains:
coolproject_data
coolproject_launchpad
__pycache__


Next, run the example task:

```powershell
python3 coolproject.py -example-task
```



## Adding new dependencies
Open up the <project_name>_info.py make any changes to the requirements that you want. And changes you make to these requirements will be picked up and the virtual environent will be updated as needed. What will happen is that the program will build your virtual enviornment in an out-of-the way location and allow you to directly call your commands without needing to invoke a virtual environment manually, which is a huge pain.


Add this for the Long Path instructions for Windows. 
https://github.com/maljefairi/Windows-Long-Path


## Windows Private Key Storage:
The private keys are stored in the OSs credential manager. To see where the private key is stored:
Open the control panel:
Control Panel.
Click "System and Security"
On the left bar, click the "User Accounts" option
In the Credential Manager, click the "Manage Windows Credentials" option.
Scroll down. Find the "Generic Credentials" section.
You'll see your launchpad credentials there.


## Troubleshooting

### ValueError: RSA key format is not supported
You might have made a mistake if you copied your private key over to a server. That can happen and if there's a trailing whitespace or a missing dash in delimiters, it will complain.

#### Exception: Version mismatch: this is the 'cffi' package version 1.17.1, located in '/blah/venv_linux_wsl2/lib/python3.9/site-packages/cffi/api.py'. When we import the top-level '_cffi_backend' extension module, we get version 1.14.0, located in '/usr/lib/python3/dist-packages/_cffi_backend.cpython-38-x86_64-linux-gnu.so'.  The two versions should be equal; check your installation.

https://foss.heptapod.net/pypy/cffi/-/issues/540

I tried adding the cffi 1.14 dependency to the linux wsl2, in the project info.py file but it didn't work.

https://dev.to/ask_dba/comment/jnd9
sudo pip3 install cffi==1.14

No dice I tried that.

https://forum.seafile.com/t/seahub-fails-to-start-cffi-issue/17154
python3 -m pip install --force-reinstall --upgrade --target <SOMEWHERE>/seafile-server-9.0.5/seahub/thirdpart cffi==1.14.6




