$ErrorActionPreference = "Stop"

$appDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$scriptPath = Join-Path $appDirectory "simon_says.py"
$iconPath = Join-Path $appDirectory "simon_says.ico"
$installedIconDirectory = Join-Path $env:LOCALAPPDATA "SimonSays"
$installedIconPath = Join-Path $installedIconDirectory "simon_says.ico"
$desktopPath = [Environment]::GetFolderPath("Desktop")
$shortcutPath = Join-Path $desktopPath "Simon Says.lnk"

$python = Get-Command pythonw.exe -ErrorAction SilentlyContinue
if (-not $python) {
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
}

if (-not $python) {
    throw "Python was not found on PATH. Install Python and run this script again."
}

New-Item -ItemType Directory -Path $installedIconDirectory -Force | Out-Null
Copy-Item -LiteralPath $iconPath -Destination $installedIconPath -Force

$shell = New-Object -ComObject WScript.Shell
$shortcut = $shell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $python.Source
$shortcut.Arguments = "`"$scriptPath`""
$shortcut.WorkingDirectory = $appDirectory
$shortcut.IconLocation = "$installedIconPath,0"
$shortcut.Description = "Play Simon Says"
$shortcut.Save()

Write-Host "Created desktop shortcut: $shortcutPath"
