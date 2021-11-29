#!/usr/bin/python

from practicemode import keymap, keyboards, key, uinput
from evdev import ecodes
from select import select
import sys

leftShift = False
rightShift = False

def isShifted(
):
    return leftShift or rightShift

ACTION_RELEASE = 0
ACTION_PRESS = 1

def onEvent(
    _uinput,
    _EVENT,
):
    global leftShift, rightShift

    if event.type != ecodes.EV_KEY:
        return False

    if event.code == ecodes.KEY_LEFTSHIFT:
        if event.value == ACTION_RELEASE:
            leftShift = False
        elif event.value == ACTION_PRESS:
            leftShift = True

        return True
    elif event.code == ecodes.KEY_RIGHTSHIFT:
        if event.value == ACTION_RELEASE:
            rightShift = False
        elif event.value == ACTION_PRESS:
            rightShift = True

        return True

    GENERATE_KEY = key.Unshifted if isShifted() == False else key.Shifted

    FROM_KEY = GENERATE_KEY( event.code )

    if FROM_KEY not in KEYMAP:
        return False

    if event.value != ACTION_PRESS:
        return True

    TO_KEY = KEYMAP[ FROM_KEY ]

    SHIFT_ACTION = ACTION_PRESS if TO_KEY.SHIFTED == True else ACTION_RELEASE

    uinput.sendKeyEvent(
        _uinput,
        ecodes.KEY_RIGHTSHIFT,
        SHIFT_ACTION,
    )

    uinput.sendKeyEvent(
        _uinput,
        TO_KEY.CODE,
        ACTION_PRESS,
    )

    uinput.sendKeyEvent(
        _uinput,
        TO_KEY.CODE,
        ACTION_RELEASE,
    )

    uinput.sendSync( _uinput )

    return True

KEYMAP_PATH = sys.argv[ 1 ] if len( sys.argv ) >= 2 else 'keymap.py'

KEYMAP = keymap.read( KEYMAP_PATH )

keyboards = keyboards.enum()

uinput_ = uinput.uinput()

for keyboard in keyboards:
    keyboard.grab()

while True:
    try:
        readableKeyboards, _, _ = select(
            keyboards[:],
            [],
            [],
        )

        for readableKeyboard in readableKeyboards:
            for event in readableKeyboard.read():
                if onEvent(
                    uinput_,
                    event,
                ) == False:
                    uinput.sendEvent(
                        uinput_,
                        event,
                    )

                    uinput.sendSync( uinput_ )
    except KeyboardInterrupt:
        for keyboard in keyboards:
            keyboard.ungrab()

        raise
