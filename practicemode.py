#!/usr/bin/python

from practicemode import keymap, keyboards, uinput, event
import argparse

argumentParser = argparse.ArgumentParser()
argumentParser.add_argument(
    '-v',
    dest = 'verbose',
    default = False,
    action = 'store_true',
)
argumentParser.add_argument(
    'keymap',
    nargs = '?',
    metavar = 'keymap.py',
)

ARGS = argumentParser.parse_args()

KEYMAP_PATH = ARGS.keymap
VERBOSE = ARGS.verbose

KEYMAP = keymap.read( KEYMAP_PATH ) if KEYMAP_PATH is not None else {}

keyboards = keyboards.enum()

uinput = uinput.uinput()

for keyboard in keyboards:
    keyboard.grab()

try:
    event.loop(
        VERBOSE,
        KEYMAP,
        keyboards,
        uinput,
    )
except:
    for keyboard in keyboards:
        keyboard.ungrab()

    raise
