# windows-desktop-shortcut-cleaner
Python 3 script for Windows that removes all shortcuts from the user's Desktop folder, with optional exceptions.

A lot of Windows apps will create shortcuts on the desktop without asking the user for permission. Scheduling this script can help with keeping the desktop clean automatically.

# Requirements
* Windows 10 or newer (anything newer than Windows Vista probably works, but not supported)
* Python ^3.9

# Installation
Using [pipx](https://github.com/pypa/pipx):
```cmd
REM Installation
pip install -U pipx
pipx install git+https://github.com/Rainyan/windows-desktop-shortcut-cleaner

REM Running
scleaner

REM Updating
pipx upgrade scleaner
```

Using git:
```cmd
REM Installation
git clone https://github.com/Rainyan/windows-desktop-shortcut-cleaner
CD ".\windows-desktop-shortcut-cleaner"

REM Running
python src\cleaner.py

REM Updating
git pull
```

# Usage
For a simple dry-run (doesn't delete anything), simply run the app.

If you installed with pipx, the command is `scleaner`.

If you're using the script version, run the script with `python src\cleaner.py` (or `python3`, if `python` doesn't work for your environment).

If your dry-run printout returns empty, the tool would have deleted nothing. Else, you'll see a list of would-be deleted files:
```cmd
>scleaner
[Dry-run] Would remove: "C:\Users\username\Desktop\ALVR.lnk"
[Dry-run] Would remove: "C:\Users\username\Desktop\Mingw haskell shell.lnk"
```

If you don't want to delete specific shortcuts, add them to your exceptions list:
```cmd
>scleaner --exceptions "ALVR,Mingw haskell shell"
```

Once you're happy with the dry-run output, you can delete the files for real with the `-f` flag:
```cmd
>scleaner --exceptions "ALVR,Mingw haskell shell" -f
```

## Full list of available commands
```
usage: scleaner [-h] [-f] [-V] [-d DESKTOPS] [-e EXCEPTIONS] [--print-my-desktop-dir]

Python script that removes all shortcuts from the user's Desktop folder, with optional exceptions

options:
  -h, --help            show this help message and exit
  -f, --no-dry-run      permanently delete the matching files (instead of dry-run). default: false
  -V, --verbose         whether to print additional debug information. default: false
  -d DESKTOPS, --desktops DESKTOPS
                        comma-delimited list of desktop identifiers to use. default: Desktop,PublicDesktop
  -e EXCEPTIONS, --exceptions EXCEPTIONS
                        comma-delimited list of shortcuts never to be deleted, without the .lnk extension. default:
                        empty list
  --print-my-desktop-dir
                        outputs the user's desktop directory to stdout and exits
```

## More examples
If you'd like to skip deleting shortcuts from the public desktop folder, you can specify the folders to be scanned with `-d/--desktops`:
```cmd
REM This will skip "PublicDesktop", and only scan the user's own desktop folder.
>scleaner --desktops "Desktop"
```


## Scheduling

### Powershell
#### Add the scheduled task


> [!NOTE]  
> You may have to modify the file paths in this snippet to match your system.

This example is using the pythonw interpreter, instead of the pipx binary.

```ps1
# Set your python path and the script path here.
# Note that you can use "pythonw" instead of "python" in Windows
# to prevent the console window popup for background tasks.
$action = New-ScheduledTaskAction `
  -Execute "$env:LOCALAPPDATA\Programs\Python\Python311\pythonw.exe" `
  -WorkingDirectory "$env:USERPROFILE\code\windows-desktop-shortcut-cleaner\src" `
  -Argument "cleaner.py -f -e `"Exception One,bar,baz`""

# Scheduling a daily cleanup at 6 AM here, see the docs for customizing:
# https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasktrigger
$trigger = New-ScheduledTaskTrigger -Daily -At 6:00am
$trigger.StartBoundary = [DateTime]::Parse($trigger.StartBoundary).ToLocalTime().ToString("s")

$settings = New-ScheduledTaskSettingsSet

Register-ScheduledTask -Action $action -Trigger $trigger -Settings $settings `
  -TaskName "Cleanup Desktop Shortcuts" `
  -Description "Removes unwanted .lnk shortcuts from the desktop folder(s)."
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
  * The `src/thirdparty` directory is exempt from this rule.
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
