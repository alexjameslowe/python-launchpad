import os
import subprocess

def vshell():
  copiedEnv = os.environ.copy()

  subprocess.run(
    ["python3"],
    env=copiedEnv,
    check=True
  )