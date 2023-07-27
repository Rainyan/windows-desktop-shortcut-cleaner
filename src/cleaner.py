#!/usr/bin/env python3

"""Python 3 script for removing shortcuts from the Desktop folder on Windows."""

# MIT License
#
# Copyright (c) 2023 Rain
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


import thirdparty.knownpaths as kp

import os

# Never delete shortcuts with these names
EXCEPTIONS = (
    "ALVR",
    "AutoProcPrio with better rules",
    "Install GHC dev dependencies",
    "Mingw haskell shell",
    "MuseScore 4",
    "SideQuest",
)


def is_in_exceptions(x):
    """Return whether x (sans .lnk extension, case insensitive) is in EXCEPTIONS"""
    return x.split(".lnk")[0].lower() in (a.lower() for a in EXCEPTIONS)


def get_desktop_path():
    """Get the Desktop path of the current user"""
    return kp.get_path(
        getattr(kp.FOLDERID, "Desktop"), getattr(kp.UserHandle, "current")
    )


def main(verbose=True):
    """Entry point"""
    desktop_path = get_desktop_path()
    assert os.path.isdir(desktop_path)
    removed = []
    for f in os.listdir(desktop_path):
        if any((os.path.islink(f), os.path.isfile(f), os.path.isdir(f))):
            continue
        if not f.endswith(".lnk"):
            continue
        if is_in_exceptions(f):
            continue
        remove_file(os.path.join(desktop_path, f))
        removed.append(f)
    if verbose:
        print(f"Cleaned {len(removed)} desktop shortcut(s)")
        for f in removed:
            print(f'- "{os.path.join(desktop_path, f)}"')


def remove_file(f, dry_run=False):
    """Remove a file, with optional dry_run option for debug"""
    if dry_run:
        print(f'[Dry-run] Would remove: "{f}"')
        return
    os.remove(f)


if __name__ == "__main__":
    main()
