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

## Acknowledgements
This script was made possible by this useful utility: https://gist.github.com/mkropat/7550097,
included and used here under the MIT License.

Full license text for this `src/thirdparty/knownpaths.py` file:
> The MIT License (MIT)
> 
> Copyright (c) 2014 Michael Kropat
> 
> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
> 
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
> 
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
