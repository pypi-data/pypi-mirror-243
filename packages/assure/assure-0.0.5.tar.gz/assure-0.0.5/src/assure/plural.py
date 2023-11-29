__all__ = [
    'singular',
    'plural',
]

Singular = str | int | float | bytes | bool

def singular(o):
    if isinstance(o, Singular):
        return o
    else:
        [o] = o
        return singular(o)

def plural(o):
    if not isinstance(o, Singular):
        return o
    else:
        return [o]
