param(
  [int]$Limit = 0,
  [switch]$NoSkipExisting
)

$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$Python = "D:\Desktop\EdgeDetection\my_env\python.exe"
$InputDir = "D:\Desktop\去水印所有藻类图像"
$Manifest = Join-Path $RepoRoot "metrics\manifests\full_algae_dewatermark_v1_cv2_readable_candidate.txt"
$ParamsJson = Join-Path $RepoRoot "experiments\optimization_v1\configs\locked_full506_final_mainline.json"
$OutputDir = Join-Path $RepoRoot "experiments\full-algae-dewatermark-v1\outputs\cv2readable2770\runs\full2770_locked_final_mainline"
$LogDir = Join-Path $OutputDir "logs"
$LogPath = Join-Path $LogDir "full2770_locked_final_mainline.log"

$ArgsList = @(
  "main.py",
  "--input-dir", $InputDir,
  "--manifest", $Manifest,
  "--params-json", $ParamsJson,
  "--output-dir", $OutputDir
)

if ($Limit -gt 0) {
  $ArgsList += @("--limit", [string]$Limit)
}

if (-not $NoSkipExisting) {
  $ArgsList += "--skip-existing"
}

Write-Host "[INFO] RepoRoot: $RepoRoot"
Write-Host "[INFO] InputDir: $InputDir"
Write-Host "[INFO] Manifest: $Manifest"
Write-Host "[INFO] ParamsJson: $ParamsJson"
Write-Host "[INFO] OutputDir: $OutputDir"
Write-Host "[INFO] LogPath: $LogPath"
Write-Host "[INFO] Limit: $Limit"
Write-Host "[INFO] SkipExisting: $(-not $NoSkipExisting)"

Push-Location $RepoRoot
try {
  New-Item -ItemType Directory -Force -Path $LogDir | Out-Null
  "[$(Get-Date -Format s)] Stage1 full-pool run start" | Tee-Object -FilePath $LogPath -Append
  "Python: $Python" | Tee-Object -FilePath $LogPath -Append
  "Args: $($ArgsList -join ' ')" | Tee-Object -FilePath $LogPath -Append
  & $Python @ArgsList 2>&1 | Tee-Object -FilePath $LogPath -Append
  if ($LASTEXITCODE -ne 0) {
    throw "Stage1 full-pool run failed with exit code $LASTEXITCODE"
  }
  "[$(Get-Date -Format s)] Stage1 full-pool run completed" | Tee-Object -FilePath $LogPath -Append
}
finally {
  Pop-Location
}
