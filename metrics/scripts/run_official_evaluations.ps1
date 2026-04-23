Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# This entrypoint is only for the current formal enhancement + protocol-v2 evaluation workflow.
# It should not be treated as the canonical interpreter for every historical script in the repo.
# It rebuilds official manifests and overwrites the two formal evaluation output directories.
$Root = (Resolve-Path (Join-Path $PSScriptRoot "..\\..")).Path
$PythonExe = "D:\\Desktop\\EdgeDetection\\my_env\\python.exe"
$Runner = Join-Path $Root "metrics\\scripts\\run_official_evaluations.py"
& $PythonExe $Runner
