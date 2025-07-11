
# Python Launchpad
The purpose of this library is to provide a base from which you can write a python program that does three important everyday things:

## 1.
Launches a background subprocess which completes a long-running process and shows a report table to the user as its working

## 2. 
Manages virutal-environments behind the scenes. It will install them and activate them behind the scenes so that you don't have to do that. You just run the commands from your system python >= 3.5 and the meat of the program will be run in a virtual environment that you don't have to set up yourself.

## 3.
Works on window and linux.
Note: Still needs some work before it will run on linux.


## Installation
cd to your project folder.
Make sure that the following entries are in your gitignore:

python-launchpad/
<project-name-here>_settings.json

<project-name-here> is a standin for a project handle that you decide. Python Launchpad will add some files to your project directory and this handle is a convenience so that you can easily distinguish launchpad files from other things in your directory. E.g., there will be a "coolproject_info.py", "coolproject_tasks.py" etc.

```powershell
python3 .\python-launchpad\main.py -init coolproject
```

You'll notice that some files appear, among them coolproject_settings.json.

Open this file up. It will look like this:

```json
{
  "launchpad_handle":"postitivepay",
  "system_python_handle":"python3",
  "python_location_for_venv":"C:/Program Files/Python310"
}
```
1. The launchpad handle. This is the name of the main entry point that will will run commands against.

2. "system_python_handle": This is the alias of python that your CLI session uses by default. Often this is "python" or "python3"

3. "python_location_for_venv": Python Launchpad will handle the virtual environment and keep it out of the way. In this field you'll specify which version of python you want the virtual environment to use.

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




This will build your virtual enviornment in an out-of-the way location and allow you to directly call your commands without needing to invoke a virtual environment. In addition, any changes you make to the requirments in Info.py will be picked up and the virtual environent will be updated as needed.


Add this for the Long Path instructions for Windows. 
https://github.com/maljefairi/Windows-Long-Path

# Troubleshooting

Exception: Version mismatch: this is the 'cffi' package version 1.17.1, located in '/blah/venv_linux_wsl2/lib/python3.9/site-packages/cffi/api.py'.  When we import the top-level '_cffi_backend' extension module, we get version 1.14.0, located in '/usr/lib/python3/dist-packages/_cffi_backend.cpython-38-x86_64-linux-gnu.so'.  The two versions should be equal; check your installation.

https://foss.heptapod.net/pypy/cffi/-/issues/540

I tried adding the cffi 1.14 dependency to the linux wsl2, in the project info.py file but it didn't work.

https://dev.to/ask_dba/comment/jnd9
sudo pip3 install cffi==1.14

No dice I tried that.

https://forum.seafile.com/t/seahub-fails-to-start-cffi-issue/17154
python3 -m pip install --force-reinstall --upgrade --target <SOMEWHERE>/seafile-server-9.0.5/seahub/thirdpart cffi==1.14.6