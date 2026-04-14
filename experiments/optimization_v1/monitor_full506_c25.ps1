param(
    [Parameter(Mandatory = $true)]
    [string[]]$Pids
)

$ErrorActionPreference = "Continue"
$Root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$LogDir = Join-Path $Root "experiments\optimization_v1\logs"
$StatusPath = Join-Path $LogDir "full506_c25_monitor_status.txt"
$EvalStdout = Join-Path $LogDir "full506_c25_eval_stdout.log"
$EvalStderr = Join-Path $LogDir "full506_c25_eval_stderr.log"
$PythonExe = "D:\Desktop\EdgeDetection\my_env\python.exe"

New-Item -ItemType Directory -Force -Path $LogDir | Out-Null

function Write-Status {
    param([string]$Message)
    $stamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    Add-Content -Path $StatusPath -Value "[$stamp] $Message" -Encoding UTF8
}

$PidList = @()
foreach ($pidText in $Pids) {
    foreach ($part in ($pidText -split ",")) {
        $trimmed = $part.Trim()
        if ($trimmed) {
            $PidList += [int]$trimmed
        }
    }
}

Write-Status "Monitor started. Waiting for PIDs: $($PidList -join ', ')"

foreach ($pidValue in $PidList) {
    try {
        $proc = Get-Process -Id $pidValue -ErrorAction SilentlyContinue
        if ($proc) {
            Write-Status "Waiting for PID $pidValue"
            Wait-Process -Id $pidValue
            Write-Status "PID $pidValue exited"
        } else {
            Write-Status "PID $pidValue was not running"
        }
    } catch {
        Write-Status "Wait failed for PID ${pidValue}: $($_.Exception.Message)"
    }
}

$FinalDir = Join-Path $Root "results_optimized_c25\png\Final"
$FinalCount = 0
if (Test-Path $FinalDir) {
    $FinalCount = (Get-ChildItem -Path $FinalDir -File -ErrorAction SilentlyContinue | Measure-Object).Count
}
Write-Status "Final PNG count after enhancement: $FinalCount"

if ($FinalCount -eq 506) {
    Write-Status "Starting full506 evaluation"
    $args = @(
        "metrics\evaluate_protocol_v2.py",
        "--quiet",
        "--original-dir", "data\inputImg\Original",
        "--result-dir", "results_optimized_c25\png\Final",
        "--method-name", "c25_full506",
        "--output-dir", "metrics\outputs\evaluate_protocol_v2\full506_c25"
    )
    $evalProc = Start-Process -FilePath $PythonExe -ArgumentList $args -WorkingDirectory $Root -RedirectStandardOutput $EvalStdout -RedirectStandardError $EvalStderr -PassThru
    Write-Status "Evaluation PID: $($evalProc.Id)"
    Wait-Process -Id $evalProc.Id
    Write-Status "Evaluation exited with process id $($evalProc.Id). Check metrics\outputs\evaluate_protocol_v2\full506_c25"
} else {
    Write-Status "Not starting evaluation because Final PNG count is not 506"
}
