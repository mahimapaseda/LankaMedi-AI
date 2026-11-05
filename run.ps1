<#
.SYNOPSIS
    LankaMedi AI - Local Web Server Runner (PowerShell)

.DESCRIPTION
    Automates environment verification, dependency checking, .env configuration,
    and starts the Flask server for LankaMedi AI on Windows.

.PARAMETER Port
    Optional custom port to run on (e.g. -Port 8080). Defaults to .env PORT or 5000.

.PARAMETER HostName
    Optional host address (default: 127.0.0.1).

.PARAMETER NoBrowser
    Switch to prevent opening the browser automatically.

.EXAMPLE
    .\run.ps1
    .\run.ps1 -Port 8000
    .\run.ps1 -NoBrowser
#>

[CmdletBinding()]
param (
    [int]$Port = 0,
    [string]$HostName = "127.0.0.1",
    [switch]$NoBrowser
)

$ErrorActionPreference = "Stop"
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location -LiteralPath $ScriptDir

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   LankaMedi AI - Clinical Decision-Support Assistant" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan

# Step 1: Detect Python Interpreter
Write-Host "[+] " -ForegroundColor Green -NoNewline
Write-Host "Checking Environment: " -ForegroundColor Yellow -NoNewline
Write-Host "Detecting Python installation..." -ForegroundColor White

$PythonCmd = $null
$Candidates = @("python", "py", "python3")
foreach ($cmd in $Candidates) {
    try {
        $testVer = & $cmd --version 2>&1
        if ($LASTEXITCODE -eq 0 -and $testVer -match "Python\s+3\.") {
            $PythonCmd = $cmd
            break
        }
    } catch {}
}

if (-not $PythonCmd) {
    Write-Host "[X] Python 3 was not found in PATH." -ForegroundColor Red
    Write-Host "Please install Python 3.10+ from https://www.python.org/downloads/ and check 'Add to PATH'." -ForegroundColor Yellow
    exit 1
}

$PyVersion = (& $PythonCmd --version 2>&1).Trim()
Write-Host "[v] Found $PyVersion using '$PythonCmd'" -ForegroundColor Green

# Step 2: Virtual Environment Check
$VenvPython = Join-Path $ScriptDir ".venv\Scripts\python.exe"
if (Test-Path -LiteralPath $VenvPython) {
    Write-Host "[+] " -ForegroundColor Green -NoNewline
    Write-Host "Virtual Environment: " -ForegroundColor Yellow -NoNewline
    Write-Host "Found active venv at .venv" -ForegroundColor White
    $PythonCmd = $VenvPython
}

# Step 3: Verify & Load Configuration (.env)
Write-Host "[+] " -ForegroundColor Green -NoNewline
Write-Host "Configuration: " -ForegroundColor Yellow -NoNewline
Write-Host "Checking .env file..." -ForegroundColor White

$EnvFile = Join-Path $ScriptDir ".env"
$EnvExample = Join-Path $ScriptDir ".env.example"

if (-not (Test-Path -LiteralPath $EnvFile)) {
    if (Test-Path -LiteralPath $EnvExample) {
        Copy-Item -LiteralPath $EnvExample -Destination $EnvFile
        Write-Host "[!] Created .env from .env.example. Add your NVIDIA_API_KEY if needed." -ForegroundColor DarkYellow
    } else {
        Write-Host "[!] No .env file found. Application will use default configuration." -ForegroundColor DarkYellow
    }
} else {
    Write-Host "[v] Configuration file (.env) detected." -ForegroundColor Green
}

# Read Port from .env if not explicitly specified
if ($Port -eq 0) {
    if (Test-Path -LiteralPath $EnvFile) {
        $MatchLine = Get-Content -LiteralPath $EnvFile | Where-Object { $_ -match "^PORT\s*=\s*(\d+)" } | Select-Object -First 1
        if ($MatchLine -and $MatchLine -match "^PORT\s*=\s*(\d+)") {
            $Port = [int]$Matches[1]
        }
    }
    if ($Port -eq 0) {
        $Port = 5000
    }
}

# Step 4: Verify Python Dependencies
Write-Host "[+] " -ForegroundColor Green -NoNewline
Write-Host "Dependencies: " -ForegroundColor Yellow -NoNewline
Write-Host "Verifying installed packages..." -ForegroundColor White

$TestScript = "import flask, pydantic, pypdf, PIL, requests, dotenv; print('OK')"
$CheckResult = & $PythonCmd -c $TestScript 2>&1

if ($LASTEXITCODE -ne 0 -or $CheckResult -notmatch "OK") {
    Write-Host "[!] Missing packages detected. Installing from requirements.txt..." -ForegroundColor DarkYellow
    $ReqFile = Join-Path $ScriptDir "requirements.txt"
    & $PythonCmd -m pip install -r $ReqFile
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[X] Failed to install dependencies. Please run manually: pip install -r requirements.txt" -ForegroundColor Red
        exit 1
    }
    Write-Host "[v] All dependencies installed successfully." -ForegroundColor Green
} else {
    Write-Host "[v] All core dependencies verified: Flask, Pydantic, PyPDF, Pillow, Requests, python-dotenv" -ForegroundColor Green
}

# Step 5: Check Port Availability
$PortInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue | Where-Object { $_.State -eq "Listen" }
if ($PortInUse) {
    $OldPort = $Port
    $Port = $Port + 1
    Write-Host "[!] Port $OldPort is in use. Auto-switching to port $Port." -ForegroundColor DarkYellow
}

# Step 6: Start Server & Launch Browser
$ServerUrl = "http://${HostName}:${Port}"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   Server Ready to Accept Requests" -ForegroundColor White
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "   Local Web URL:   " -NoNewline -ForegroundColor White
Write-Host "$ServerUrl" -ForegroundColor Cyan
Write-Host "   Health Check:    " -NoNewline -ForegroundColor White
Write-Host "$ServerUrl/api/v1/health" -ForegroundColor Cyan
Write-Host "   Languages:       " -NoNewline -ForegroundColor White
Write-Host "English, Sinhala, Tamil (trilingual)" -ForegroundColor Yellow
Write-Host "   Emergency:       " -NoNewline -ForegroundColor White
Write-Host "Hotline 1990 (Suwa Seriya) Integrated" -ForegroundColor Green
Write-Host ""
Write-Host "   [Press Ctrl+C to stop the local server]" -ForegroundColor DarkGray
Write-Host ""

if (-not $NoBrowser) {
    Start-Job -ScriptBlock {
        param($TargetUrl)
        Start-Sleep -Seconds 2
        Start-Process $TargetUrl
    } -ArgumentList $ServerUrl | Out-Null
}

$env:PORT = "$Port"
$env:FLASK_RUN_HOST = "$HostName"
$env:FLASK_RUN_PORT = "$Port"

$AppFile = Join-Path $ScriptDir "app.py"
& $PythonCmd $AppFile
