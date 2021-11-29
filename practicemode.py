#!/usr/bin/python

from evdev import InputDevice, list_devices, ecodes
from evdev.uinput import UInput
from select import select
from practicemode import key
import sys

def evalFile(
    _PATH,
):
    with open(
        _PATH,
        'rb',
    ) as f:
        return eval(
            compile(
                f.read(),
                _PATH,
                'eval',
            ),
        )

def getDevicesFromPaths(
    _DEVICE_PATHS,
):
    return [ InputDevice( DEVICE_PATH ) for DEVICE_PATH in _DEVICE_PATHS ]

def isKeyboard(
    _device,
):
    if _device.name == 'py-evdev-uinput':
        return False

    CAPABILITIES = _device.capabilities( verbose = False )

    if 1 not in CAPABILITIES:
        return False

    SUPPORTED_KEYS = CAPABILITIES[ 1 ]
    if ecodes.KEY_SPACE not in SUPPORTED_KEYS:
        return False
    elif ecodes.KEY_A not in SUPPORTED_KEYS:
        return False
    elif ecodes.KEY_Z not in SUPPORTED_KEYS:
        return False
    elif ecodes.BTN_MOUSE in SUPPORTED_KEYS:
        return False

    return True

def selectDevices(
):
    allDevices = getDevicesFromPaths( list_devices() )

    filteredDevices = list(
        filter(
            isKeyboard,
            allDevices,
        )
    )

    if not filteredDevices:
        raise RuntimeError( 'input device not found' )

    return filteredDevices

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

CONFIG_FILE = sys.argv[ 1 ] if len( sys.argv ) >= 2 else 'config.py'

KEYMAP = evalFile( CONFIG_FILE )

KEYBOARD_CODES = ecodes.keys.keys() - ecodes.BTN

uinput = UInput(
    events = {
        ecodes.EV_KEY: KEYBOARD_CODES,
    }
)

devices = selectDevices()
for device in devices:
    device.grab()

while True:
    try:
        readableDevices, _, _ = select(
            devices[:],
            [],
            [],
        )

        for readableDevice in readableDevices:
            for event in readableDevice.read():
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
        for device in devices:
            device.ungrab()

        raise
