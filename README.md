# windows-desktop-shortcut-cleaner
Python 3 script for Windows that removes all shortcuts from the user's Desktop folder, with an optional exceptions list.

A lot of Windows apps will create shortcuts on the desktop without asking the user. Scheduling this script will help keeping the desktop clean automatically.

# Usage

## One-time run
Assuming the correct "python" version is callable from PATH in this example
```cmd
python src\cleaner.py
```

## Scheduling
Open Powershell as current user, and enter:
```ps1
# Set your python path and the script path here.
# Note that you can use "pythonw" instead of "python" in Windows
# to prevent the console window popup for background tasks.
$action = New-ScheduledTaskAction `
  -Execute "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe" `
  -Argument "$env:USERPROFILE\code\windows-desktop-shortcut-cleaner\src\cleaner.py"

$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$trigger.StartBoundary = [DateTime]::Parse($trigger.StartBoundary).ToLocalTime().ToString("s")

$settings = New-ScheduledTaskSettingsSet

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings `
  -TaskName "Cleanup Desktop Shortcuts" `
  -Description "Removes unwanted .lnk shortcuts from the user's Desktop folder."
```
