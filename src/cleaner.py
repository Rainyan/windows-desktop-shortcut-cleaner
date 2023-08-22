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

import argparse
import os


# Flip this to False to actually remove the files!
DRY_RUN = True
# Print extra info to stdout
VERBOSE = False
# Desktop identifiers to use
DESKTOP_IDS = ["Desktop", "PublicDesktop"]
# Never delete shortcuts with these names
EXCEPTIONS = []


def is_in_exceptions(x):
    """Return whether x (sans .lnk extension, case insensitive) is in EXCEPTIONS"""
    return x.split(".lnk")[0].lower() in (a.lower() for a in EXCEPTIONS)


def get_known_path(folderid):
    """Get the Desktop path of the current user"""
    return kp.get_path(
        getattr(kp.FOLDERID, folderid), getattr(kp.UserHandle, "current")
    )


def main():
    """Entry point"""
    parser = argparse.ArgumentParser(
        prog="scleaner",
        description="Python script that removes all shortcuts from the user's Desktop folder, with optional exceptions",
    )
    parser.add_argument(
        "-f",
        "--no-dry-run",
        action="store_true",
        help="permanently delete the matching files (instead of dry-run)",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="whether to print additional debug information",
    )
    parser.add_argument(
        "-d",
        "--desktops",
        help="comma-delimited list of desktop identifiers to use",
    )
    parser.add_argument(
        "-e",
        "--exceptions",
        help="never delete shortcuts with these names",
    )
    parser.add_argument(
        "--print-my-desktop-dir",
        action="store_true",
        help="outputs the user's desktop directory to stdout and exits",
    )
    args = parser.parse_args()

    if args.print_my_desktop_dir:
        desktop = get_known_path("Desktop")
        assert os.path.isdir(desktop)
        print(desktop)
        return

    global VERBOSE
    VERBOSE = args.verbose

    global DRY_RUN
    DRY_RUN = not args.no_dry_run

    global DESKTOP_IDS
    if args.desktops is not None:
        DESKTOP_IDS = []  # Because we overwrite the default list
        for a in list(set((args.desktops).split(","))):
            a = a.strip()
            if not a in DESKTOP_IDS:
                DESKTOP_IDS.append(a)

    global EXCEPTIONS
    if args.exceptions is not None:
        for a in list(set((args.exceptions).split(","))):
            a = a.strip()
            assert not a.endswith(
                ".lnk"
            ), "Please don't include the .lnk extension to the exception name"
            if not a in EXCEPTIONS:
                EXCEPTIONS.append(a)

    desktop_paths = [get_known_path(a) for a in DESKTOP_IDS]
    assert all(os.path.isdir(a) for a in desktop_paths)

    if VERBOSE:
        print(f"{len(desktop_paths)} desktop paths total: {desktop_paths}")

    for desktop_path in desktop_paths:
        if VERBOSE:
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
            remove_file(full_path)
            removed.append(f)
        if VERBOSE:
            print(
                f"{'[Dry-run] Would remove' if DRY_RUN else 'Removed'} {len(removed)} desktop shortcut(s)."
            )
            for f in removed:
                print(f'- "{os.path.join(desktop_path, f)}"')
            print()


def remove_file(f):
    """Remove a file, with optional dry_run option for debug"""
    assert os.path.isfile(f)
    if DRY_RUN:
        print(f'[Dry-run] Would remove: "{f}"')
        return
    os.remove(f)


if __name__ == "__main__":
    main()
