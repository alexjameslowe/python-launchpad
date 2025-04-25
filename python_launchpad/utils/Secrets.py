########################################################################
##
##  A utility for creating public and private keys and coordinating
##  with the keyring utility to store the private key on the os's
##  keychain and allowing the program to safely store and retrieve
##  sensitive secrets
##
########################################################################


from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP, AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
from keyring import get_password, set_password

from python_launchpad.utils.Configure import getSecretsDirectory, getSecretsManifest, getMainSetting, getPublicKeyPath, getSecretsFilePath
from python_launchpad.utils.Utils import readJSON
from python_launchpad.utils.Format import isWindows, joinPath
from os import path
import json
from base64 import b64decode,b64encode
import binascii
import re


PUBLIC_KEY = None
SECRETS = None
CACHED_DECRYPTED = None
AES_SUFFIX = "__aes"
SECRETS_MANIFEST = None


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
def readSecretsManifestJSON():
  global SECRETS_MANIFEST
  if(not SECRETS_MANIFEST):

    secretsManifestURI = getSecretsManifest()

    if(path.isfile(secretsManifestURI)):
      SECRETS_MANIFEST = readJSON(secretsManifestURI)


##
# write the main secrets file
#
def writeSecretsManifestJSON():
  with open(getSecretsManifest(), 'w') as secretsManifestFile:

    if(SECRETS_MANIFEST != None):
      json.dump(SECRETS_MANIFEST, secretsManifestFile)
    else:
      secretsManifestFile.write('{}')

    secretsManifestFile.close()



##
# Adapted from
# https://gist.github.com/lopes/168c9d74b988391e702aac5f4aa69e41?permalink_comment_id=2835739
#
# https://cryptobook.nakov.com/symmetric-key-ciphers/aes-encrypt-decrypt-examples
# https://pycryptodome.readthedocs.io/en/latest/src/examples.html
#
#
def aesSymmetricEncrypt(msgUTF8):
    aesKey = get_random_bytes(16)

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aesKey, AES.MODE_CBC, iv)

    cipherTextUTF8 = b64encode(iv + cipher.encrypt(pad(msgUTF8.encode('utf-8'), AES.block_size))).decode('utf-8')

    return cipherTextUTF8, aesKey


def aesSymmetricDecrypt(cipherTextUTF8, aesKey):
    raw = b64decode(cipherTextUTF8.encode())

    cipher = AES.new(aesKey, AES.MODE_CBC, raw[:AES.block_size])
    decryptedUTF8 = unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode('utf-8')

    return decryptedUTF8


##
# Encrypt a secret
#
# https://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
# https://medium.com/@info_82002/a-beginners-guide-to-encryption-and-decryption-in-python-12d81f6a9eac
#
# For solving confusion about how the key should be serialized and reacquired when storing it as a string
# https://stackoverflow.com/questions/21327491/using-pycrypto-how-to-import-a-rsa-public-key-and-use-it-to-encrypt-a-string
#
# For the excellent suggestion of using hybrid encryption to get around the length limitations
# with RSA encryption.
# https://stackoverflow.com/questions/65856980/python-rsa-message-encryption-plaintext-is-too-long
#
def setSecret(key, value, asjson=False, asBatch=False):

  aesPosInKey = None
  try: 
    aesPosInKey = key.index(AES_SUFFIX)
  except:
    pass 

  if(not re.match( r'^([A-Za-z0-9_\-]+)$', key)):
    raise Exception(f"Key must be letters, numbers, _ or -. You passed in. {key}")

  #Why did the user do that? Complain.
  if(aesPosInKey != None):
    raise Exception(f"You can't have a key with the string {AES_SUFFIX}")

  #We first encrypt text symmetrically. 
  ciphertextUTF8, aesKey = aesSymmetricEncrypt(str(value) if asjson == False else json.dumps(value))

  publicKeyObj = RSA.importKey(getPublicKey())

  cipherRSA = PKCS1_OAEP.new(publicKeyObj)

  #Now we're going to encrypt the aes key *asymmetrically*
  cipherTextUTFOfAESKey = b64encode( cipherRSA.encrypt( aesKey ) ).decode("utf-8")

  cipherTextMainURI = joinPath(getSecretsDirectory(), f"{key}.txt")
  cipherTextAESURI = joinPath(getSecretsDirectory(), f"{key}{AES_SUFFIX}.txt")

  with open(cipherTextMainURI, 'w') as s1:
    s1.write(ciphertextUTF8)
  s1.close()

  with open(cipherTextAESURI, 'w') as s2:
    s2.write(cipherTextUTFOfAESKey)
  s2.close()

  readSecretsManifestJSON()

  if not key in SECRETS_MANIFEST: 
    SECRETS_MANIFEST.append(key)
    writeSecretsManifestJSON()
  


##
# Decrypt a secret
#
#
def getSecret(key, defval=None, asjson=False, asint=False, asbool=False, asfloat=False, ascsvlist=False):
  
  global CACHED_DECRYPTED

  if(CACHED_DECRYPTED == None):
    CACHED_DECRYPTED = {}

  cached = CACHED_DECRYPTED.get(key, None)

  if(cached != None):
    return cached 
  
  cipherTextMainURI = joinPath(getSecretsDirectory(), f"{key}.txt")
  cipherTextAESURI = joinPath(getSecretsDirectory(), f"{key}{AES_SUFFIX}.txt")

  if(not path.isfile(cipherTextMainURI) or not path.isfile(cipherTextAESURI)):
    print(f"No secret for key: {key}")
    return 

  with open(cipherTextMainURI) as s1:
    cipherTextMainUTF8 = s1.read()
  s1.close()

  with open(cipherTextAESURI) as s2:
    cipherTextAESUTF8 = s2.read()
  s2.close()
  
  if(cipherTextMainUTF8 == None):
    return defval
  
  if(cipherTextAESUTF8 == None):
    raise Exception("Missing the aes key for this secret. This could indicate that something happened when switching versions.")
  
  cipherBytes = b64decode(cipherTextAESUTF8)
  
  cipherRSA = PKCS1_OAEP.new(RSA.import_key(getPrivateKey()))

  #Note that these are the bytes of the aes key, not the decoded utf-8 string.
  aesKey = cipherRSA.decrypt(cipherBytes) 

  #now that the aesKey has been decoded, we're going to decrypt the actual secret with the aes-key
  varContentsUTF8 = aesSymmetricDecrypt(cipherTextMainUTF8, aesKey)

  #Now perform the typing/serialization
  varToReturn = None

  if(asjson):
    varToReturn = {} if varContentsUTF8 == None or varContentsUTF8 == 'None' else json.loads(varContentsUTF8)
  elif(asint):
    varToReturn = 0 if varContentsUTF8 == None or varContentsUTF8 == 'None' else int(varContentsUTF8)
  elif(asfloat):
    varToReturn = 0 if varContentsUTF8 == None or varContentsUTF8 == 'None' else float(varContentsUTF8)
  elif(asbool):
    varToReturn = str(varContentsUTF8) == "True"
  elif(ascsvlist):
    varContentsUTF8NoNone = '' if varContentsUTF8 == None or varContentsUTF8 == 'None' else varContentsUTF8
    splitsky = varContentsUTF8NoNone.split(',')
    varToReturn = [] if splitsky == None else splitsky
  else:
    varToReturn = varContentsUTF8

  CACHED_DECRYPTED[key] = varToReturn 

  return varToReturn



##
# List the secrets
#
#
def listSecrets():
  
  readSecretsManifestJSON()
  print("*************************")
  print("* ")
  print("*  Listing Secrets")
  print("* ")

  for secretName in SECRETS_MANIFEST: 
    print(f"* {secretName}")
  
  print("* ")
  print("*************************")


