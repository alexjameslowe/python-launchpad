PRODUCT_NAME = "test-product"
PRODUCT_NICE_TITLE = "Test Product"
VERSION = "1.0.0"
HELP_EMAIL = "alexjameslowe@gmail.com"
AUTHOR = "Alex Lowe"

def RESOLVE_WINDOWS_ENVIRONMENT():
  return "windows"

def RESOLVE_MAC_ENVIRONMENT():
  return "mac"

def RESOLVE_LINUX_ENVIRONMENT():
  return "wsl2"


REQUIREMENTS = {
  "windows": {
    "windows": [
      "pandas==1.5.2",
      "rich==13.7.0",
    ]
  },
  "mac": {
    "mac": [
      "pandas==1.5.2",
      "rich==13.7.0",
    ]
  },
  "linux": {
    "wsl2": [
      "pandas==1.5.2",
      "rich==13.7.0",    
    ],
    "ubuntu": [
      "pandas==1.5.2",
      "rich==13.7.0",    
    ]
  }
}



## Take care not to edit anything below this line unless you really really mean to.
#https://pypi.org/project/keyring/
#macOS keychain supports macOS 11 (Big Sur) and later requires Python 3.8.7 or later with the "universal2" binary. See #525 for details.

BASE_REQUIREMENTS = {
  "windows": {
    "windows": [
      "portalocker==2.8.2",
      "pywin32==303",
      "pycryptodome==3.21.0",
      "keyring==25.6.0"
    ]
  },
  "mac": {
    "mac": [
      "portalocker==2.8.2",
      "pycryptodome==3.21.0",
      "keyring==25.6.0"
    ]
  },
  "linux": {
    "wsl2": [
      "portalocker==2.8.2",
      "pycryptodome==3.21.0",
      "keyring==25.6.0" 
    ],
    "ubuntu": [
      "portalocker==2.8.2",
      "pycryptodome==3.21.0",
      "keyring==25.6.0"  
    ]
  }
}

