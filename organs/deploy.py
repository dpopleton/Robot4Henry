#!/usr/bin/env python3
"""
Copy an organ's firmware to its Pico: everything in organs/<organ>/firmware/
plus the shared organs/pico_common/, all flat in the Pico's root (they
import each other by bare name), then restart it so main.py runs.

Usage:
    python organs/deploy.py eyes                       # first Pico found
    python organs/deploy.py eyes --port /dev/ttyACM1
    python organs/deploy.py eyes --dry-run             # just list the files

Needs mpremote (pip install mpremote) and MicroPython already on the Pico
(see the organ's README). Close anything else holding the port first.
"""

import argparse
import glob
import os
import subprocess
import sys

ORGANS = os.path.dirname(os.path.abspath(__file__))


def firmware_files(organ):
    folder = os.path.join(ORGANS, organ, "firmware")
    if not os.path.isdir(folder):
        raise SystemExit(f"No firmware folder for {organ!r}: {folder}")
    files = sorted(glob.glob(os.path.join(folder, "*.py")))
    shared = sorted(glob.glob(os.path.join(ORGANS, "pico_common", "*.py")))
    names = {}
    for path in files + shared:
        name = os.path.basename(path)
        if name == "__init__.py":
            continue
        if name in names:
            raise SystemExit(f"{name} is in both {names[name]} and {path} — they'd overwrite each other on the Pico")
        names[name] = path
    return [names[name] for name in sorted(names)]


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("organ", help="folder name under organs/, e.g. eyes")
    parser.add_argument("--port", default="auto", help="serial port (default: the first Pico mpremote finds)")
    parser.add_argument("--dry-run", action="store_true", help="list the files without copying")
    args = parser.parse_args()

    files = firmware_files(args.organ)
    for path in files:
        print(os.path.relpath(path, os.path.dirname(ORGANS)), flush=True)
    if args.dry_run:
        return
    # A full reset, not soft-reset: mpremote's soft-reset leaves the Pico at its
    # prompt instead of running main.py.
    command = ["mpremote", "connect", args.port, "fs", "cp", *files, ":", "+", "reset"]
    sys.exit(subprocess.call(command))


if __name__ == "__main__":
    main()
