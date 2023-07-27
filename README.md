# windows-desktop-shortcut-cleaner
Python 3 script for Windows that removes all shortcuts from the user's Desktop folder, with an optional exceptions list.

A lot of Windows apps will create shortcuts on the desktop without asking the user. Scheduling this script will help keeping the desktop clean automatically.

# Usage
Assuming "python" is in PATH and refers to your Python executable.

## Running the script
Type in your command prompt
`python src\cleaner.py`

## Scheduling the script
Open Powershell as current user, and enter:
```ps1
# Set your python path and the script path here.
# Note that you can use "pythonw" instead of "python" in Windows
# to prevent the console window popup for bg tasks.
$action = New-ScheduledTaskAction `
  -Execute "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe" `
  -Argument "C:\code\windows-desktop-shortcut-cleaner\src\cleaner.py"

$trigger = New-ScheduledTaskTrigger -Daily -At 6:00pm
$trigger.StartBoundary = [DateTime]::Parse($trigger.StartBoundary).ToLocalTime().ToString("s")

$settings = New-ScheduledTaskSettingsSet

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings `
  -TaskName "Cleanup Desktop Shortcuts" `
  -Description "Removes unwanted .lnk shortcuts from the user's Desktop folder."
```
