
# Python Launchpad
The purpose of this library is to provide a base from which you can write a python program that does three important everyday things:

## 1.
Launches a background subprocess which completes a long-running process and shows a report table to the user as its working

## 2. 
Manages virutal-environments behind the scenes. It will install them and activate them behind the scenes so that you don't have to do that. You just run the commands from your system python >= 3.5 and the meat of the program will be run in a virtual environment that you don't have to set up yourself.

## 3.
Works on window and linux.
Note: Still needs some work before it will run on linux.

Windows:
The private keys are stored in the OSs credential manager.
Open the control panel:
Control Panel.
Click "System and Security"
On the left bar, click the "User Accounts" option
In the Credential Manager, click the "Manage Windows Credentials" option.
Scroll down. Find the "Generic Credentials" section.
You'll see your launchpad credentials there.



## Installation
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


## Getting this working on linux (Ubuntu)

Getting this error on the ubuntu server:
keyring.errors.NoKeyringError: No recommended backend was available. Install a recommended 3rd party backend package; or, install the keyrings.alt package if you want to use the non-recommended backends. See https://pypi.org/project/keyring for details.

On Linux, the KWallet backend relies on dbus-python, which does not always install correctly when using pip (compilation is needed). For best results, install dbus-python as a system package.
https://pypi.org/project/keyring/



AI response:

The keyring.errors.NoKeyringError: No recommended backend was available error in Python's keyring library indicates that the library could not find a suitable backend to store and retrieve passwords or secrets in your environment. 
Explanation: 
The keyring library aims to provide a secure way to manage credentials by integrating with system-level keyrings or password managers (like macOS Keychain, GNOME Keyring/Secret Service on Linux, or Windows Credential Manager). When this error occurs, it means keyring was unable to detect or connect to any of these recommended, secure backends. 
Common Causes and Solutions: 

• Missing System Keyring/Password Manager: 
	• Linux: You might be missing a desktop environment's keyring service (e.g., GNOME Keyring or KWallet) or the necessary D-Bus components. Install gnome-keyring or similar packages for your desktop environment. 
	• Server Environments/Containers: If you're running keyring in a headless environment (like a server or Docker container) without a graphical desktop, there's no system keyring available. In this case, you'll need to either: 
		• Install and configure a keyring daemon like gnome-keyring-daemon and manage its D-Bus session. 
		• Consider using an alternative backend provided by keyrings.alt (see below) if security requirements allow for less robust storage. 

• Missing Python Bindings for Backends: 
	• Even if the system keyring is installed, keyring might need specific Python packages to interact with it. For instance, secretstorage is required for the Secret Service backend (used by GNOME Keyring). Ensure these are installed: 

        pip install secretstorage

• Virtual Environment Issues: 
	• If you're using a virtual environment, ensure that the necessary system packages (like dbus-python) are accessible within it. You might need to create the virtual environment with the --system-site-packages flag or selectively install the required system packages within the virtual environment. 

• No Recommended Backend Available (Alternative Backends): 
	• If no recommended backend is suitable or available in your environment, you can opt to use alternative, less secure backends by installing keyrings.alt. 
	• Caution: Backends in keyrings.alt (like PlaintextKeyring) might store credentials in plain text or less secure ways. Only use these if you understand the security implications and it aligns with your application's security requirements. 
	• To use keyrings.alt: 

        pip install keyrings.alt

Then, you might need to explicitly set the desired keyring using keyring.set_keyring() in your code if the default selection doesn't pick the one you intend. 

• Running as a Service/Cron Job: 
	• When running Python scripts as system services or cron jobs, they might not have access to the user's graphical session and its associated keyring. Consider how your service or job is configured and if it has the necessary environment variables and permissions to interact with a keyring. You might need to adjust the environment or use a different credential management strategy for such scenarios. 

AI responses may include mistakes.

