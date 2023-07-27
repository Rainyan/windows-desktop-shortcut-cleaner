#!/usr/bin/env python3

"""Python 3 script for removing shortcuts from the Desktop folder on Windows."""

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
