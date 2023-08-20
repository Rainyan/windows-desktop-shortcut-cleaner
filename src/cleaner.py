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

# Flip this to False to actually remove the files!
DRY_RUN = True
# Whether to also clean the public desktop (visible to all users)
INCLUDE_PUBLIC_DESKTOP = True
# Print extra info to stdout
VERBOSE = True


def is_in_exceptions(x):
    """Return whether x (sans .lnk extension, case insensitive) is in EXCEPTIONS"""
    return x.split(".lnk")[0].lower() in (a.lower() for a in EXCEPTIONS)


def get_known_path(folderid):
    """Get the Desktop path of the current user"""
    return kp.get_path(
        getattr(kp.FOLDERID, folderid), getattr(kp.UserHandle, "current")
    )


def main(dry_run, include_public_desktop, verbose):
    """Entry point"""
    desktop_paths = [get_known_path("Desktop")]
    if include_public_desktop:
        desktop_paths.append(get_known_path("PublicDesktop"))

    if verbose:
        print(f"{len(desktop_paths)} desktop paths total: {desktop_paths}")

    for desktop_path in desktop_paths:
        if verbose:
            print(f'Checking desktop path: "{desktop_path}"')
        assert os.path.isdir(desktop_path)
        removed = []
        for f in os.listdir(desktop_path):
            full_path = os.path.join(desktop_path, f)
            if any((os.path.islink(full_path), os.path.isdir(full_path))):
                continue
            if not f.endswith(".lnk"):
                continue
            if is_in_exceptions(f):
                continue
            remove_file(full_path, dry_run)
            removed.append(f)
        if verbose:
            print(
                f"{'[Dry-run] Would remove' if dry_run else 'Removed'} {len(removed)} desktop shortcut(s)."
            )
            for f in removed:
                print(f'- "{os.path.join(desktop_path, f)}"')


def remove_file(f, dry_run):
    """Remove a file, with optional dry_run option for debug"""
    if dry_run:
        print(f'[Dry-run] Would remove: "{f}"')
        return
    os.remove(f)


if __name__ == "__main__":
    main(DRY_RUN, INCLUDE_PUBLIC_DESKTOP, VERBOSE)
