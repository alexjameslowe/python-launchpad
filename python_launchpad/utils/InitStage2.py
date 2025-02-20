###########################################################################
##
##  InitStage2 
##
##  This sets up the public and private key for storing secrets securely
##  
##  Author Alex Lowe
##
###########################################################################


from python_launchpad.utils.Secrets import generateKeys, getSecretsFileKeyPath

def init(password):

  

  generateKeys(password)
  
