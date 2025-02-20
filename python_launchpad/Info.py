PRODUCT_NAME = "test-product"
PRODUCT_NICE_TITLE = "Test Product"
VERSION = "1.0.0"
HELP_EMAIL = "alexjameslowe@gmail.com"
AUTHOR = "Alex Lowe"

WIN_REQUIREMENTS = [
  "pandas==1.5.2",
  "rich==13.7.0",
]

LIN_REQUIREMENTS = [
  "pandas==1.5.2",
  "rich==13.7.0",
]


## Take care not to edit anything below this line unless you really really mean to.

#https://pypi.org/project/keyring/
#macOS keychain supports macOS 11 (Big Sur) and later requires Python 3.8.7 or later with the “universal2” binary. See #525 for details.

BASE_WIN_REQUIREMENTS = [
  "portalocker==2.8.2",
  "pywin32==303",
  "pycryptodome==3.21.0",
  "keyring==25.6.0"
]

BASE_LIN_REQUIREMENTS = [
  "pycryptodome==3.21.0",
  "keyring==25.6.0"
]

