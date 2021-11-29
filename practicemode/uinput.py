from evdev import ecodes
from evdev.uinput import UInput

def uinput(
):
    KEYBOARD_CODES = ecodes.keys.keys() - ecodes.BTN

    return UInput(
        events = {
            ecodes.EV_KEY: KEYBOARD_CODES,
        }
    )

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
