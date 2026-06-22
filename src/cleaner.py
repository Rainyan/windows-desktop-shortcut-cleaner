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

FIRST_CHAR_OF_EXT = "."


def is_in_exceptions(x, extensions):
    """Return whether x (sans extension(s), case insensitive) is in EXCEPTIONS"""
    for exception in EXCEPTIONS:
        for ext in extensions:
            if x.split(f"{FIRST_CHAR_OF_EXT}{ext}")[0].lower() in exception.lower():
                return True
    return False


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
        help="permanently delete the matching files (instead of dry-run). default: false",
    )
    parser.add_argument(
        "-V",
        "--verbose",
        action="store_true",
        help="whether to print additional debug information. default: false",
    )
    parser.add_argument(
        "-d",
        "--desktops",
        help="comma-delimited list of desktop identifiers to use. default: Desktop,PublicDesktop",
    )
    parser.add_argument(
        "-e",
        "--exceptions",
        help="comma-delimited list of shortcuts never to be deleted, with file extension being optional unless ambiguous. default: empty list",
    )
    parser.add_argument(
        "-E",
        "--extensions",
        help='comma-delimited list of dot-prefixed file extensions which to consider as shortcut files, for example: "lnk,url" default: lnk',
        default="lnk",
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
        for a in listify(args.desktops):
            a = a.strip()
            if a not in DESKTOP_IDS:
                DESKTOP_IDS.append(a)

    extensions = listify(args.extensions)
    global EXCEPTIONS
    if args.exceptions is not None:

        def without_ext(x):
            return FIRST_CHAR_OF_EXT.join(x.split(FIRST_CHAR_OF_EXT)[:-1])

        for a in listify(args.exceptions):
            a = a.strip()
            unambiguous = a.split(FIRST_CHAR_OF_EXT)[-1] in extensions
            potentially_ambiguous = not unambiguous
            if potentially_ambiguous:
                for exception in EXCEPTIONS:
                    if without_ext(a) == "":
                        continue
                    assert without_ext(a) != without_ext(exception), (
                        f'"{a}" is ambiguous with "{exception}", '
                        "please exclude with file extension included"
                    )
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
            if not any((f.endswith(ext) for ext in extensions)):
                continue
            if is_in_exceptions(f, extensions):
                continue
            remove_file(full_path, extensions)
            removed.append(f)
        if VERBOSE:
            print(
                f"{'[Dry-run] Would remove' if DRY_RUN else 'Removed'} {len(removed)} desktop shortcut(s)."
            )
            for f in removed:
                print(f'- "{os.path.join(desktop_path, f)}"')
            print()


def listify(delimited_str, unique=True, allow_empty=False, delimiter=","):
    """For a delimited string, return a list of its elements.

    If "unique" is True, omits identical elements from the output.
    If "allow_empty" is False, omits empty elements from the output.
    """

    def fn_set(x):
        return set(x) if unique else x

    def fn_filter(x):
        return x if allow_empty else filter(None, x)

    return list(fn_set(fn_filter(delimited_str.split(delimiter))))


def remove_file(path, allowed_file_extensions):
    """Remove a file, with optional dry_run option for debug"""
    assert os.path.isfile(path)
    for ext in allowed_file_extensions:
        assert len(ext) > 0
    assert any((path.endswith(ext) for ext in allowed_file_extensions))
    if DRY_RUN:
        print(f'[Dry-run] Would remove: "{path}"')
        return
    os.remove(path)


if __name__ == "__main__":
    main()
