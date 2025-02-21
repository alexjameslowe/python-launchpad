###########################################################################
##
##  InitStage2 
##
##  This sets up the public and private key for storing secrets securely
##  
##  Author Alex Lowe
##
###########################################################################


from python_launchpad.utils.Secrets import generateKeys
from python_launchpad.utils.Configure import getMainSetting

def init():

  print(" ")
  print(" ")
  print(" ")
  print("**********************************************************")
  print("* ")
  print("* Generating public and private key for secrets")
  print("* ")
  try:
    generateKeys()
  except Exception as err:
    print(f"Error: {str(err)}")
  print("**********************************************************")
  
