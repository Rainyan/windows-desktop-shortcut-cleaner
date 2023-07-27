# windows-desktop-shortcut-cleaner
Python 3 script for Windows that removes all shortcuts from the user's Desktop folder, with optional exceptions.

A lot of Windows apps will create shortcuts on the desktop without asking the user. Scheduling this script will help keeping the desktop clean automatically.

# Requirements
* Modern-ish version of Windows (newer than Vista should work)
* Modern-ish version of Python 3 (tested with 3.11)

# Install
Get the code:
```cmd
git clone https://github.com/Rainyan/windows-desktop-shortcut-cleaner
```

Try the [one-time run](#one-time-run) to do a dry-run of the script, which will just print what would have been deleted instead of actually deleting it.

If you get no printout, no files would have been deleted. Else, there should be printout akin to:
```
[Dry-run] Would remove: "calc.exe.lnk"
[Dry-run] Would remove: "notepad.exe.lnk"
```

If you're happy with the output, flip the dry-run switch off in code to start deleting things for real:
```py
# Flip this to False to actually remove the files!
DRY_RUN = True
```

# Usage
## Exceptions
You can customize the list of shortcuts that will be preserved by modifying the EXCEPTIONS global in the source code:
```py
# Never delete shortcuts with these names
EXCEPTIONS = (
    "ALVR",
    "AutoProcPrio with better rules",
    "Install GHC dev dependencies",
    "Mingw haskell shell",
    "MuseScore 4",
    "SideQuest",
    # etc...
)
```
These exceptions are case-insensitive, and should not include the `.lnk` shortcut extension.

## One-time run
Assuming the correct "python" version is callable from PATH in this example
```cmd
python src\cleaner.py
```

## Scheduling

### Powershell
#### Add the scheduled task


> [!NOTE]  
> You may have to modify the file paths in this snippet to match your system.


```ps1
# Set your python path and the script path here.
# Note that you can use "pythonw" instead of "python" in Windows
# to prevent the console window popup for background tasks.
$action = New-ScheduledTaskAction `
  -Execute "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe" `
  -Argument "$env:USERPROFILE\code\windows-desktop-shortcut-cleaner\src\cleaner.py"

# Scheduling a daily cleanup at 6 AM here, see the docs for customizing:
# https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasktrigger
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$trigger.StartBoundary = [DateTime]::Parse($trigger.StartBoundary).ToLocalTime().ToString("s")

$settings = New-ScheduledTaskSettingsSet

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings `
  -TaskName "Cleanup Desktop Shortcuts" `
  -Description "Removes unwanted .lnk shortcuts from the user's Desktop folder."
```
#### Remove the scheduled task
```ps1
Unregister-ScheduledTask -TaskName "Cleanup Desktop Shortcuts"
```

### Task Scheduler
If you'd prefer a graphical user interface, you can instead use the *Task Scheduler* app, which comes preinstalled with most Windows systems.

## Contributing
PRs welcome!

* Please format your code with [black](https://github.com/psf/black).
* If you're making substantial changes, please open an issue for discussing them before submitting a patch.

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
