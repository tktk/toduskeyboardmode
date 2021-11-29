from . import key
from evdev import ecodes

def read(
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
