# param (
#   [Parameter(Mandatory=$true)][string]$param1,
#   [Parameter(Mandatory=$true)][string]$param2
# )

$scriptURI = $MyInvocation.MyCommand.Path
$scriptDir = Split-Path $scriptURI -Parent

python3 "$scriptDir\..\..\main.py" -wsl-bridge-generate-keys
