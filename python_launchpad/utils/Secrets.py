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

from python_launchpad.utils.Configure import getMainSetting, getPublicKeyPath, getSecretsFilePath
from python_launchpad.utils.Format import joinPath
from python_launchpad.utils.Utils import readJSON
from os import path
import json
from base64 import b64decode,b64encode

PUBLIC_KEY = None
SECRETS = None
CACHED_DECRYPTED = None


def getServiceName():
  launchHandle = getMainSetting("launch_handle")
  if(launchHandle == None):
    raise Exception("launch_handle is missing fro the main config json")
  
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
def generateKeys(password):

  global PUBLIC_KEY

  # Generate RSA keys
  key = RSA.generate(2048)
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
      secretsFile.write('[]')

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
def encrypt(key, value, asjson=False, asBatch=False):
  readSecretsJSON()

  keyB64Decoded = b64decode(getPublicKey())
  publicKeyObj = RSA.importKey(keyB64Decoded)

  cipherRSA = PKCS1_OAEP.new(publicKeyObj)
  cipherText = cipherRSA.encrypt( str(value) if asjson == False else json.dumps(value) )

  SECRETS[key] = cipherText

  if(asBatch == False):
    writeSecretsJSON()


##
# Decrypt a secret
#
#
def decrypt(key, defval=None, asjson=False, asint=False, asbool=False, asfloat=False, ascsvlist=False):
 
  readSecretsJSON()

  cached = CACHED_DECRYPTED.get(key, None)

  if(cached != None):
    return cached 

  cipherText = SECRETS.get(key, None)

  if(cipherText == None):
    return defval
  
  keyB64Decoded = b64decode(getPrivateKey())
  
  cipherRSA = PKCS1_OAEP.new(RSA.import_key(keyB64Decoded))

  varContents = cipherRSA.decrypt(cipherRSA)

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



  















def encrypt(msg):
  pass
