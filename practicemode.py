#!/usr/bin/python

from practicemode import keymap, keyboards, uinput, event
import sys

KEYMAP_PATH = sys.argv[ 1 ] if len( sys.argv ) >= 2 else 'keymap.py'

KEYMAP = keymap.read( KEYMAP_PATH )

keyboards = keyboards.enum()

uinput = uinput.uinput()

for keyboard in keyboards:
    keyboard.grab()

try:
    event.loop(
        KEYMAP,
        keyboards,
        uinput,
    )
except:
    for keyboard in keyboards:
        keyboard.ungrab()

    raise
