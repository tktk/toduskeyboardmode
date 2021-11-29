#!/usr/bin/python

from practicemode import keymap, keyboards, key
from evdev import ecodes
from evdev.uinput import UInput
from select import select
import sys

def sendSync(
    _uinput,
):
    _uinput.syn()

def sendEvent(
    _uinput,
    _EVENT,
):
    _uinput.write_event( _EVENT )
    sendSync( _uinput )

def sendKeyEvent(
    _uinput,
    _CODE,
    _VALUE,
):
    _uinput.write(
        ecodes.EV_KEY,
        _CODE,
        _VALUE,
    )

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

    sendKeyEvent(
        _uinput,
        ecodes.KEY_RIGHTSHIFT,
        SHIFT_ACTION,
    )

    sendKeyEvent(
        _uinput,
        TO_KEY.CODE,
        ACTION_PRESS,
    )

    sendKeyEvent(
        _uinput,
        TO_KEY.CODE,
        ACTION_RELEASE,
    )

    sendSync( uinput )

    return True

KEYMAP_PATH = sys.argv[ 1 ] if len( sys.argv ) >= 2 else 'keymap.py'

KEYMAP = keymap.read( KEYMAP_PATH )

KEYBOARD_CODES = ecodes.keys.keys() - ecodes.BTN

keyboards = keyboards.enum()

uinput = UInput(
    events = {
        ecodes.EV_KEY: KEYBOARD_CODES,
    }
)

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
                    uinput,
                    event,
                ) == False:
                    sendEvent(
                        uinput,
                        event,
                    )

                    sendSync( uinput )
    except KeyboardInterrupt:
        for keyboard in keyboards:
            keyboard.ungrab()

        raise
