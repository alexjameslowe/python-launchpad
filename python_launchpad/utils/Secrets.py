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

from python_launchpad.utils.Configure import getMainSetting, getPublicKeyPath, getSecretsFilePath
from python_launchpad.utils.Utils import readJSON
from python_launchpad.utils.Format import isWindows
from os import path
import json
from base64 import b64decode,b64encode
import binascii


PUBLIC_KEY = None
SECRETS = None
CACHED_DECRYPTED = None
AES_SUFFIX = "__aes"


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



def aesSymmetricEncrypt(data):
    aesKey = get_random_bytes(16)

    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(aesKey, AES.MODE_CBC, iv)

    # cipherText = b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size)))

    cipherText = b64encode(iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))).decode('utf-8')

    return cipherText, aesKey

def aesSymmetricDecrypt(data, aesKey):
    raw = b64decode(data)
    cipher = AES.new(aesKey, AES.MODE_CBC, raw[:AES.block_size])
    decrypted = unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size).decode('utf-8')

    return decrypted

# https://pycryptodome.readthedocs.io/en/latest/src/examples.html
# perform a symmetric encryption
#
def aesSymmetricEncrypt_(msg):
  
  bytesToEncrypt = msg.encode()

  #This will give us a 128bit key.
  aesKey = get_random_bytes(16)

  cipher = AES.new(aesKey, AES.MODE_CTR)

  #ciphertextHex = cipher.encrypt(bytesToEncrypt).hex()
  #ciphertextHex = binascii.hexlify(cipher.encrypt(bytesToEncrypt)).decode('utf-8')

  cipherTextBytes = cipher.encrypt(bytesToEncrypt)

  cipher2 = AES.new(aesKey, AES.MODE_CTR)
  #decrypted = cipher2.decrypt( binascii.unhexlify(ciphertextHex.encode()) )
  decrypted = cipher2.decrypt( cipherTextBytes ).decode('utf-8')
  print('Decrypted!!!', decrypted)

  return "testing", aesKey


# Decrypt symmetrically
#
# https://cryptobook.nakov.com/symmetric-key-ciphers/aes-encrypt-decrypt-examples
#
def aesSymmetricDecrypt_(cipherTextUTF8, aesKey):

  cipher = AES.new(aesKey, AES.MODE_CTR)

  #decryptedMsgUTF8 = cipher.decrypt(cipherTextUTF8.encode())

  #decryptedMsgUTF8 = cipher.decrypt( bytes.fromhex(cipherTextUTF8))

  #decryptedMsgUTF8 = cipher.decrypt( binascii.unhexlify(cipherTextUTF8.encode()) )

  decryptedMsgUTF8 = cipher.decrypt( binascii.unhexlify(cipherTextUTF8.encode()) )
  

  print("ALEX hey what's this? ")
  print(decryptedMsgUTF8)

  hex_string = decryptedMsgUTF8 #b64decode( binascii.hexlify(decryptedMsgUTF8).decode('utf-8') )


  return hex_string #decryptedMsgUTF8


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

# def setSecret(key, value, asjson=False, asBatch=False):

#   global SECRETS 

#   readSecretsJSON()

#   if(SECRETS == None):
#     SECRETS = {}

#   publicKeyObj = RSA.importKey(getPublicKey())

#   cipherRSA = PKCS1_OAEP.new(publicKeyObj)

#   mgToEncrypt = str(value) if asjson == False else json.dumps(value)
#   bytesToEncrypt = mgToEncrypt.encode('utf-8')

#   cipherText = b64encode( cipherRSA.encrypt( bytesToEncrypt ) ).decode("utf-8")

#   SECRETS[key] = cipherText

#   if(asBatch == False):
#     writeSecretsJSON()
def setSecret(key, value, asjson=False, asBatch=False):

  global SECRETS 

  aesPosInKey = None
  try: 
    aesPosInKey = key.index(AES_SUFFIX)
  except:
    pass 

  #Why did the user do that? Complain.
  if(aesPosInKey != None):
    raise Exception(f"You can't have a key with the string {AES_SUFFIX}")

  #We first encrypt text symmetrically. 
  ciphertextUTF8, aesKey = aesSymmetricEncrypt(str(value) if asjson == False else json.dumps(value))

  print("AES Key ENCRYPT")
  print(aesKey)

  readSecretsJSON()

  if(SECRETS == None):
    SECRETS = {}

  publicKeyObj = RSA.importKey(getPublicKey())

  cipherRSA = PKCS1_OAEP.new(publicKeyObj)

  #Now we're going to encrypt the aes key *asymmetrically*
  cipherTextUTFOfAESKey = b64encode( cipherRSA.encrypt( aesKey ) ).decode("utf-8")

  #Save both of these to the secrets 
  SECRETS[key] = ciphertextUTF8
  SECRETS[f"{key}{AES_SUFFIX}"] = cipherTextUTFOfAESKey

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

  cipherTextMainUTF8 = SECRETS.get(key, None)
  cipherTextAESUTF8 = SECRETS.get(f"{key}{AES_SUFFIX}", None)

  if(cipherTextMainUTF8 == None):
    return defval
  
  if(cipherTextAESUTF8 == None):
    raise Exception("Missing the aes key for this secret. This could indicate that something happened when switching versions.")
  
  cipherBytes = b64decode(cipherTextAESUTF8)
  
  cipherRSA = PKCS1_OAEP.new(RSA.import_key(getPrivateKey()))

  #Note that these are the bytes of the aes key, not the decoded utf-8 string.
  aesKey = cipherRSA.decrypt(cipherBytes) 

  print("AES Key DECRYPT")
  print(aesKey)

  #now that the aesKey has been decoded, we're going to decrypt the actual secret with the aes-key
  varContentsUTF8 = aesSymmetricDecrypt(cipherTextMainUTF8, aesKey)

  print(f"ALEX 95483 whats this? {str(varContentsUTF8)}")

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

# def getSecret(key, defval=None, asjson=False, asint=False, asbool=False, asfloat=False, ascsvlist=False):
 
#   global CACHED_DECRYPTED

#   readSecretsJSON()

#   if(CACHED_DECRYPTED == None):
#     CACHED_DECRYPTED = {}

#   cached = CACHED_DECRYPTED.get(key, None)

#   if(cached != None):
#     return cached 

#   cipherText = SECRETS.get(key, None)

#   if(cipherText == None):
#     return defval
  
#   cipherBytes = b64decode(cipherText)
  
#   cipherRSA = PKCS1_OAEP.new(RSA.import_key(getPrivateKey()))

#   varContentsUTF8 = cipherRSA.decrypt(cipherBytes).decode('utf-8')

#   varToReturn = None

#   if(asjson):
#     varToReturn = {} if varContentsUTF8 == None or varContentsUTF8 == 'None' else json.loads(varContentsUTF8)
#   elif(asint):
#     varToReturn = 0 if varContentsUTF8 == None or varContentsUTF8 == 'None' else int(varContentsUTF8)
#   elif(asfloat):
#     varToReturn = 0 if varContentsUTF8 == None or varContentsUTF8 == 'None' else float(varContentsUTF8)
#   elif(asbool):
#     varToReturn = str(varContentsUTF8) == "True"
#   elif(ascsvlist):
#     varContentsUTF8NoNone = '' if varContentsUTF8 == None or varContentsUTF8 == 'None' else varContentsUTF8
#     splitsky = varContentsUTF8NoNone.split(',')
#     varToReturn = [] if splitsky == None else splitsky
#   else:
#     varToReturn = varContentsUTF8

#   CACHED_DECRYPTED[key] = varToReturn 

#   return varToReturn