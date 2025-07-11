from python_launchpad.utils.Configure import getDataDirectory
from python_launchpad.utils.Format import joinPath
import subprocess

# Docker is a pain to interact with:
#https://stackoverflow.com/questions/44862100/need-to-run-docker-run-command-inside-python-script
#
# args
#
# dockerCMS
# The interpolated docker command string
#
# expectOutput
# default is False.
# If True, then None will be treated as success and non-none will be an error.
#
def docker(dockerCMD, expectOutput=False):

  result = None

  with open(joinPath(getDataDirectory(),'DockerOut.txt'), "w") as output: 
    output.write("")
  
  with open(joinPath(getDataDirectory(),'DockerOut.txt'), "a") as output:
    subprocess.call(dockerCMD, shell=True, stdout=output, stderr=output)
  with open(joinPath(getDataDirectory(),'DockerOut.txt'), "r") as output: 
    result = output.read()

  if(not expectOutput and result != None and str(result).strip() != ""):
    raise Exception(f"Docker: got a non-none result: {result}")
  
  return result