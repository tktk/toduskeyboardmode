from . import key, uinput
from evdev import ecodes
from select import select
import asyncio

def loop(
    _PRESS_DURATION,
    _VERBOSE,
    _KEYMAP,
    _keyboards,
    _uinput,
):
    while True:
        readableKeyboards, _, _ = select(
            _keyboards[:],
            [],
            [],
        )

        for readableKeyboard in readableKeyboards:
            for EVENT in readableKeyboard.read():
                if _onEvent(
                    EVENT,
                    _PRESS_DURATION,
                    _VERBOSE,
                    _KEYMAP,
                    _uinput,
                ) == False:
                    _redirect(
                        EVENT,
                        _VERBOSE,
                        _uinput,
                    )

_leftShift = False
_rightShift = False

def _isShifted(
):
    return _leftShift or _rightShift

_ACTION_RELEASE = 0
_ACTION_PRESS = 1

def _onEvent(
    _EVENT,
    _PRESS_DURATION,
    _VERBOSE,
    _KEYMAP,
    _uinput,
):
    global _leftShift, _rightShift

    if _EVENT.type != ecodes.EV_KEY:
        return False

    if _EVENT.code == ecodes.KEY_LEFTSHIFT:
        if _EVENT.value == _ACTION_RELEASE:
            _leftShift = False
        elif _EVENT.value == _ACTION_PRESS:
            _leftShift = True

        return True
    elif _EVENT.code == ecodes.KEY_RIGHTSHIFT:
        if _EVENT.value == _ACTION_RELEASE:
            _rightShift = False
        elif _EVENT.value == _ACTION_PRESS:
            _rightShift = True

        return True

    GENERATE_KEY = key.Unshifted if _isShifted() == False else key.Shifted

    FROM_KEY = GENERATE_KEY( _EVENT.code )

    if FROM_KEY not in _KEYMAP:
        return False

    if _EVENT.value != _ACTION_PRESS:
        return True

    TO_KEY = _KEYMAP[ FROM_KEY ]

    TO_KEY_CODE = TO_KEY.CODE

    SHIFT_ACTION = _ACTION_PRESS if TO_KEY.SHIFTED == True else _ACTION_RELEASE

    if _VERBOSE == True:
        print(
            '{0} -> {1}'.format(
                FROM_KEY,
                TO_KEY,
            )
        )

    uinput.sendKeyEvent(
        _uinput,
        ecodes.KEY_RIGHTSHIFT,
        SHIFT_ACTION,
    )

    uinput.sendKeyEvent(
        _uinput,
        TO_KEY_CODE,
        _ACTION_PRESS,
    )

    uinput.sendSync( _uinput )

    asyncio.get_event_loop().run_until_complete(
        _asyncRelease(
            _PRESS_DURATION,
            _uinput,
            TO_KEY_CODE,
        )
    )

    return True

async def _asyncRelease(
    _PRESS_DURATION,
    _uinput,
    _CODE,
):
    await asyncio.sleep( _PRESS_DURATION )

    uinput.sendKeyEvent(
        _uinput,
        _CODE,
        _ACTION_RELEASE,
    )

    uinput.sendSync( _uinput )

def _redirect(
    _EVENT,
    _VERBOSE,
    _uinput,
):
    if _VERBOSE == True:
        if _EVENT.type == ecodes.EV_KEY and _EVENT.value == _ACTION_PRESS:
            print( key.Unshifted( _EVENT.code ) )

    uinput.sendEvent(
        _uinput,
        _EVENT,
    )

    uinput.sendSync( _uinput )
