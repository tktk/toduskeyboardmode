class Key( object ):
    def __init__(
        _self,
        _CODE,
        _SHIFTED,
    ):
        _self.CODE = _CODE
        _self.SHIFTED = _SHIFTED

    def __eq__(
        _SELF,
        _OTHER,
    ):
        if not isinstance(
            _OTHER,
            Key,
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

def Unshifted(
    _CODE,
):
    return Key(
        _CODE,
        False,
    )

def Shifted(
    _CODE,
):
    return Key(
        _CODE,
        True,
    )
