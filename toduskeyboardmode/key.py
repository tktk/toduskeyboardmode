from evdev import ecodes

def Unshifted(
    _CODE,
):
    return _Key(
        _CODE,
        False,
    )

def Shifted(
    _CODE,
):
    return _Key(
        _CODE,
        True,
    )

class _Key:
    def __init__(
        _self,
        _CODE,
        _SHIFTED,
    ):
        _self.CODE = _CODE
        _self.SHIFTED = _SHIFTED

    def __str__(
        _SELF,
    ):
        return '{0}{1}'.format(
            'S-' if _SELF.SHIFTED == True else '',
            ecodes.KEY[ _SELF.CODE ],
        )

    def __eq__(
        _SELF,
        _OTHER,
    ):
        if not isinstance(
            _OTHER,
            _Key,
        ):
            return False

        if _SELF.CODE != _OTHER.CODE:
            return False

        if _SELF.SHIFTED != _OTHER.SHIFTED:
            return False

        return True

    def __hash__(
        _SELF,
    ):
        return hash(
            (
                _SELF.CODE,
                _SELF.SHIFTED,
            )
        )
