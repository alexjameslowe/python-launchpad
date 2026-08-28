
# Python Launchpad
This is a work-in-progress. The aim is to provide a base from which you can write a program that does four important things right out of the box that are a real headache to set up each time you want a new python tool:

## 1.
Launches a background subprocess which completes a long-running process and shows a report table to the user as its working

## 2. 
Provides you with a way to monitor a process, as define thread-safe variables that can be set and get by both the task and the monitor.

## 3. 
Manages virtual-environments behind the scenes. It will install them and activate them behind the scenes so that you don't have to do that. You just run the commands from your system python >= 3.9 and the meat of the program will be run in a virtual environment that you don't have to set up yourself.

## 4.
Allows multiple configurations for multiple platforms, e.g. Linux, Windows, WSL2.


## Installation

### Note for Windows WSL2 users:
#### Python usually lives in /mnt/c/Program Files and if you're running the installation commands from an Ubuntu shell, you're probably going to get an error "Permission Denied" when it attempts to create the virtual environmnet. You can either make things easy on yourself and just run the installation commands in Powershell, or you can specify a python version location that your Ubuntu shell has permissions for.

### Requirements
1. You must have requests installed on your system's python.

```bash
python -m pip install requests
```

2. You must have virtualenv installed on your system's python.

```bash
python -m pip install --user virtualenv
```

3. You must have pexpect installed
```bash
python -m pip install pexpect
```

4. If you plan to include any dependencies from git (e.g.  git+github.com/blah-blah.git), then you must have git installed.



### Windows:  Task Scheduler.
If you ever have to reschedule, note that if you do it the first time and set it to activated in a future date e.g. tomorrow morning, then it won't appear in the scheduled tasks window, which is really annoying.



### Setup Steps
1. Copy python_launchpad from the source into your project folder.

2. cd to your project folder.

3. Make sure that the following entries are in your gitignore:

python_launchpad/
<project-name-here>_settings.json
<project-name-here>_data

<project-name-here> is a standin for a project handle that you decide. Python Launchpad will add some files to your project directory and this handle is a convenience so that you can easily distinguish launchpad files from other things in your directory. E.g., there will be a "coolproject_info.py", "coolproject_tasks.py" etc.

```bash
python3 ./python_launchpad/main.py -init coolproject
```

You'll notice that some files appear, among them coolproject_settings.json.

Open this file up. It will look like this:

```json
{
  "launchpad_handle":"<my project handle>",
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
      "python_location_for_venv":"/usr/bin/python3.9",
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

```bash
python3 coolproject.py -config
```

It will configure your program. You can delete the coolproject_settings.json afterward. Note that the virtual enviornment will start building. It will also generate a public and private key for secrets. Wait until its finished.

Make sure your .gitignore contains:
coolproject_data
coolproject_launchpad
__pycache__


Next, run the example task:

```bash
python3 coolproject.py -example-task
```

## Upgrading
Run:

```bash 
python3 mycoolproject.py -upgrade
```
And it will pull a copy of the master branch make all the substitutions and get your settings moved over.

## Secret management

### Set secret

```bash
python3 mycoolproject.py -set-secret THE_SECRET_STUFF -for-key THE_NAME_OF_SECRET
```

### Overwrite secret 


```bash
python3 mycoolproject.py -set-secret THE_SECRET_STUFF -for-key THE_NAME_OF_SECRET -overwrite
```

### Get secret 

```bash
python3 mycoolproject.py -get-secret -for-key THE_NAME_OF_SECRET
```

### List secrets 

```bash
python3 mycoolproject.py -list-secrets
```

### In code,
```python
from mycoolproject_integrator.utils.Secrets import getSecret, setSecret

mysecret = getSecret('THE_NAME_OF_SECRET')

setSecret('THE_NAME_OF_SECRET', 'the new secret stuff', overwrite=True)
```

### Show private key

```bash
python3 mycoolproject.py -get-private-key
```

### Set private key
You'll make a file, enter the private key into it, save and close, and then use the -set-private-key command to set it. We do this on web-servers because I've never had any luck with setting up a key manager on Ubunutu.

So use use the above -get-private-key. It will look like this:

-----BEGIN RSA PRIVATE KEY-----
MIIEoAIBAAKCAQEA49xuTcKSnsVVwCGW/lsGzlcNyAUctSF/9d/r6hdYNM2Z+bz2
.... ...
qmdfADhDUedFnkGjWjexv2rO6jbGe/FCUPz1aa6PcTkpIf2BEdCW5nnxMbqVWncI
YoB2Q/39KxBh/FehDIfnO3qb2++5tb+BqdLLOhqJz1z0KM4x
-----END RSA PRIVATE KEY-----

Then 

```bash
touch pkey.txt
```
And 

```bash
python3 mycoolproject.y -set-private-key <location of pkey.txt>
```
It will say:
Private key logged.



### Cleanup task 
```bash
python mycoolproject.py -cleanup-task -my-cool-task
```
This is for when the task crashes in some messy or unexpected way



## Adding new dependencies
Open up the <project_name>_info.py make any changes to the requirements that you want. And changes you make to these requirements will be picked up and the virtual environent will be updated as needed. What will happen is that the program will build your virtual enviornment in an out-of-the way location and allow you to directly call your commands without needing to invoke a virtual environment manually, which is a huge pain.

Yes, you can do this in a requirments slot:
"git+https://github.com/mailchimp/mailchimp-marketing-python.git"


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

When you do a deployment to another machine, what you have to do is run -get-private-key on your machine to output the private key to the screen, and then use -set-private-key

You'll see the private key in Windows Credential Manager in <my proj>_launchpad

## Setting up your environment with Pyenv (and why you need it)
https://realpython.com/intro-to-pyenv/

The deal is that your system has it's own version of python that you don't want to mess with. At the same time, this library required Python >= 3.10. There's other python versions you projects need but you can download them and store them wherever you like.

su root 

Then run:

apt update

apt install build-essential libssl-dev zlib1g-dev \
libbz2-dev libreadline-dev libsqlite3-dev curl git \
libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev \
libffi-dev liblzma-dev

curl https://pyenv.run | bash

if .pyenv is in /root, then run

mv /root/.pyenv /home/ics \
chown -R ics:ics 

Now, exit back to your regular user.

Run these commands:

export PATH="/home/ics/.pyenv/bin:$PATH"
eval "$(pyenv init - bash)"

Append to the bottom of .profile:
export PATH="/home/ics/.pyenv/bin/:/home/ics/.pyenv/shims:$PATH"
source ~/.profile

Inside your /home/ics, you can use this:
pyenv local 3.11

Then python3 -V should always be 3.11 inside that folder, and the system is free to use the older version elsewhere.

If you want to revert back to the system's python, then in /home/ics:
rm .python-version



Then install your version:
pyenv install 3.10.0

Then use it:
pyenv 
python version 

Then use it:
pyenv global 3.10.0

python3 -V  
will say Python 3.10.0

OK ALSO WE HAVE TO INSTALL REQUESTS AND VIRTUALENV AAAAAA!!
python3 -m pip install requests
python3 -m pip install virtualenv
python3 -m pip install pexpect



## Connecting a launchpad script to crontab.

If you're using pyenv (recommended), then you're going to have to reference the version of python explicitly because crontabs environment is different and it won't have access to your pyenv shims.

So in that case here's an example:

You bash file to call your script:

```bash
#!/bin/bash

/home/youruser/.pyenv/shims/python3 /home/youruser/heartbeat-master/heartbeat.py -run-heartbeat -background
```

And your crontab. This will run every 5 minutes.

*/5 * * * * /home/ics/heartbeat.sh > heartbeat_output.txt






## Troubleshooting / Workflows

### Windows python version headaches.
pip install virtualenv
It said that I virtualenv.exe was located in C:\Users\AlexLowe\AppData\Roaming\Python\Python310\Scripts
And that should be added to PATH. So I added it to the path environment variable near the top.

### Windows _win32sysloader
If it complains that this is missing, chances are you're trying to use this with an older python version (3.8). I've seen this when trying to use watchdog. The solution is to just not use this old python version and use 3.10. 3.8 Just won't work.

### virtualenv failed. Could not migrate app data
fuel_master_2_sftp_data\venv_windows_windows"
could not migrate app data from C:\Users\...\AppData\Local\pypa\virtualenv to C:\Users\...\AppData\Local\pypa\virtualenv\Cache: Error("Cannot move a directory 'C:\\Users\\...\\AppData\\Local\\pypa\\virtualenv' into itself 'C:\\Users\\...\\AppData\\Local\\pypa\\virtualenv\\Cache'."), using old location

Something went wrong and you're using the wrong python version from the CLI with a different install of virtualenv

### Windows Task Scheduler: Failed to launch, code 101
There's a lot that can cause this. You have to give it permission to run when it's not logged on. Your user needs to have the right permissions. Finally if something goes wrong, there's a setting "Don't launch new instance" for the "if a task is already running", and that could be causing this problem. If one fails, it might leave behind a ghost task that will prevent a new one from launching. If you say "Stop the current instance" and then run it a couple of times it should clear the old one out. 


### Deployment headaches. Here's what went wrong:
### windows Error: Invalid \escape:

First thing that went wrong is that when you try and put these urls into 
the json setting file using the windows-style delimiter:
C:\Users\CoolGuy\AppData\Local\Programs\Python\Python310

You can this "Invalid \escape" error. You need to reverse the slashes:
C:/Users/CoolGuy/AppData/Local/Programs/Python/Python310

In the main.json and all your settings files.

Other thinggs that went wrong.

### The ps scripts had python3 hardcoded. 
> This needs to use the setting system_python_handle



### Switching python versions on your host machine (Less recommended)
Linux:

Note that python generally lives here: 
python versions are here: /usr/bin/

sudo apt install python3.9

Then add this line into ~/.bashrc with vi or nano or whatever:

alias python='/usr/bin/python3.9'

Now close down your host and reopen. You can verify the changes took ahold by typing 

python -V 

To make sure that the version is what you expect to see.


### 





### -get-private-key
> Another thing that went wrong is -get-private-key cut off the top line with the damn BEGIN PRIVATE RSA KEY delimiter. I had to put it back in and then hope to god that no other lines were cut off. So that's a big headache

### ValueError: RSA key format is not supported
> You might have made a mistake if you copied your private key over to a server. That can happen and if there's a trailing whitespace or a missing dash in delimiters, it will complain.

### Pip exits error 1 installation failed.
When you run a command after tinkering with the dependencies and then scary things happen when the environment refreshes like wheels fail during build, or it says installation failed at the end, it just means that your virtual environment is messed up. Go into the <my-proj>_data/vars and delete the hex-digest file, and then also go into <my_proj>_data and delete the virtual environment. The launcher will rebuild it next time you run it with any flag.


### Exception: Version mismatch: this is the 'cffi' package version 1.17.1, located in '/blah/venv_linux_wsl2/lib/python3.9/site-packages/cffi/api.py'. When we import the top-level '_cffi_backend' extension module, we get version 1.14.0, located in '/usr/lib/python3/dist-packages/_cffi_backend.cpython-38-x86_64-linux-gnu.so'.  The two versions should be equal; check your installation.

The workaround I used was to just start using python3.9 in my Ubuntu host. That might leave a bad taste I know. The whole point of venvs is that they're SEPARATE from the host. Well, this is weird frayed edge on that. Anyway you have to switch your host OS to use a version of python closer to what you have in your launcher. In my case python3.9 worked. See the above note on how to switch versions of python on your host. That should do the trick. Also, you might try that --force-reinstall and target the troublesome location of the old cffi on your host. But swtiching python versions entirely is probably cleaner.

Below is some more fixes that I read about. I'm not saying they won't work, I just didn't have any luck with them.

First, you'll be tempted to add the cffi 1.14 dependency to the linux wsl2 in the project info.py file but it will not only not work, but it will cause that environment to start throwing errors on builds.

sudo pip3 install cffi==1.17.1

*You know, this might be worth another shot*
sudo pip3 install --force-reinstall --upgrade --target <path to the place where the bad version of cffi is living> cffi==1.17.1

Alot of places including the ai say to do this:

sudo apt update
apt --fix-broken install
sudo apt install python3-dev
sudo apt install python3.8-dev

But it had no effect.

*Literature on the problem*

install python-cffi
https://stackoverflow.com/questions/58552666/exception-version-mismatch-this-is-the-cffi-package-version-1-13-1

install cffi 
https://forum.seafile.com/t/seahub-fails-to-start-cffi-issue/17154
https://dev.to/ask_dba/comment/jnd9

changing python versions
https://askubuntu.com/questions/1272870/how-can-i-change-the-default-python-on-my-ubuntu-20-04-to-python3-8

python3-dev
https://stackoverflow.com/questions/21530577/fatal-error-python-h-no-such-file-or-directory
