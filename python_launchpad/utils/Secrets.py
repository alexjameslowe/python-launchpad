########################################################################
##
##  A utility for creating public and private keys and coordinating
##  with the keyring utility to store the private key on the os's
##  keychain and allowing the program to safely store and retrieve
##  sensitive secrets
##
########################################################################


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes
from keyring import get_password, set_password

from windu_launchpad.utils.Configure import getMainSetting, getPublicKeyPath, getSecretsFilePath
from windu_launchpad.utils.Format import joinPath
from windu_launchpad.utils.Utils import readJSON
from windu_launchpad.utils.Format import isWindows
from os import path
import json
from base64 import b64decode,b64encode

PUBLIC_KEY = None
SECRETS = None
CACHED_DECRYPTED = None


def getServiceName():
  launchHandle = getMainSetting("launchpad_handle")
  if(launchHandle == None):
    raise Exception("launchpad_handle is missing fro the main config json")
  
  return f'{launchHandle}_launchpad'

def getUsername():
  return "default_user"


###
# get the public key
#
#
def getPublicKey():
  global PUBLIC_KEY

  pubKeyPath = getPublicKeyPath()

  if(PUBLIC_KEY):
    return PUBLIC_KEY 
  else:
    with open(pubKeyPath) as pubKeyFile:
      PUBLIC_KEY = pubKeyFile.read()
      pubKeyFile.close()

    if(PUBLIC_KEY == None):
      raise Exception(f"95849 failed to find public key at {pubKeyPath}")

    return PUBLIC_KEY
  

###
# get the private key from keyring utility
#
#
def getPrivateKey():
  return get_password(getServiceName(), getUsername())


##
# Write the public key
#
# 
def writePublicKey(pubKey):
  try:
    pubKeyPath = getPublicKeyPath()

    with open(pubKeyPath, 'w') as pubKeyFile:
      pubKeyFile.write(pubKey)
      pubKeyFile.close()
  
  except Exception as err:
    print("585943 Could not write public key")



## 
# Generate the public key
# TODO see if we can specify another password.
#
def generateKeys(password=None):

  global PUBLIC_KEY

  #Windows has this issue with the size of the keys
  #https://github.com/Azure/azure-sdk-for-python/issues/9857
  #keyring.set_password() fails on Windows with a 1281 character password, 
  #with the (1783, 'CredWrite', 'The stub received bad data') message, but 
  #succeeds with 1280 characters.

  # Generate RSA keys
  key = RSA.generate(1280) if isWindows() else RSA.generate(2048)
  privateKey = key.export_key(format='PEM').decode('utf-8')
  PUBLIC_KEY = key.publickey().export_key(format='PEM').decode('utf-8')

  set_password(getServiceName(), getUsername(), privateKey)

  writePublicKey(PUBLIC_KEY)


##
# write the main secrets file
#
def writeSecretsJSON():
  with open(getSecretsFilePath(), 'w') as secretsFile:

    if(SECRETS != None):
      json.dump(SECRETS, secretsFile)
    else:
      secretsFile.write('{}')

    secretsFile.close()


##
# read the main secrets file
#
def readSecretsJSON():
  global SECRETS
  if(not SECRETS):

    secretsPath = getSecretsFilePath()

    if(path.isfile(secretsPath)):
      SECRETS = readJSON(secretsPath)

##
# Encrypt a secret
#
# https://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
# https://medium.com/@info_82002/a-beginners-guide-to-encryption-and-decryption-in-python-12d81f6a9eac
#
# For solving confusion about how the key should be serialized and reacquired when storing it as a string
# https://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
def setSecret(key, value, asjson=False, asBatch=False):

  global SECRETS 

  readSecretsJSON()

  if(SECRETS == None):
    SECRETS = {}

  publicKeyObj = RSA.importKey(getPublicKey())

  cipherRSA = PKCS1_OAEP.new(publicKeyObj)

  mgToEncrypt = str(value) if asjson == False else json.dumps(value)
  bytesToEncrypt = mgToEncrypt.encode('utf-8')

  cipherText = b64encode( cipherRSA.encrypt( bytesToEncrypt ) ).decode("utf-8")

  SECRETS[key] = cipherText

  if(asBatch == False):
    writeSecretsJSON()


##
# Decrypt a secret
#
#
def getSecret(key, defval=None, asjson=False, asint=False, asbool=False, asfloat=False, ascsvlist=False):
 
  global CACHED_DECRYPTED

  readSecretsJSON()

  if(CACHED_DECRYPTED == None):
    CACHED_DECRYPTED = {}

  cached = CACHED_DECRYPTED.get(key, None)

  if(cached != None):
    return cached 

  cipherText = SECRETS.get(key, None)

  if(cipherText == None):
    return defval
  
  cipherBytes = b64decode(cipherText)
  
  cipherRSA = PKCS1_OAEP.new(RSA.import_key(getPrivateKey()))

  varContents = cipherRSA.decrypt(cipherBytes).decode('utf-8')

  varToReturn = None

  if(asjson):
    varToReturn = {} if varContents == None or varContents == 'None' else json.loads(varContents)
  elif(asint):
    varToReturn = 0 if varContents == None or varContents == 'None' else int(varContents)
  elif(asfloat):
    varToReturn = 0 if varContents == None or varContents == 'None' else float(varContents)
  elif(asbool):
    varToReturn = str(varContents) == "True"
  elif(ascsvlist):
    varContentsNoNone = '' if varContents == None or varContents == 'None' else varContents
    splitsky = varContentsNoNone.split(',')
    varToReturn = [] if splitsky == None else splitsky
  else:
    varToReturn = varContents

  CACHED_DECRYPTED[key] = varToReturn 

  return varToReturn

