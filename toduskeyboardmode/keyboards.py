from evdev import InputDevice, list_devices, ecodes

def enum(
):
    ALL_DEVICES = _enumAllDevices()

    KEYBOARDS = list(
        filter(
            _isKeyboard,
            ALL_DEVICES,
        )
    )

    if len( KEYBOARDS ) <= 0:
        raise RuntimeError( 'keyboards not found' )

    return KEYBOARDS

def _enumAllDevices(
):
    return [ InputDevice( DEVICE_PATH ) for DEVICE_PATH in list_devices() ]

def _isKeyboard(
    _DEVICE,
):
    CAPABILITIES = _DEVICE.capabilities( verbose = False )

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
