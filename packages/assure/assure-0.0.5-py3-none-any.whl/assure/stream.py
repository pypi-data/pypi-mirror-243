__all__ = [
    'seekable',
    'mode',
]

import os
import io
import pathlib

def seekable(o):
    if hasattr(o, 'seekable'):
        if o.seekable():
            return o
        if o.mode == 'r':
            return io.StringIO(o.read())
        if o.mode == 'rb':
            return io.BytesIO(o.read())
        raise TypeError(f"bad input: {o!r}")
    if isinstance(o, pathlib.Path):
        o = o.read_bytes()
    if isinstance(o, str) and os.path.exists(o):
        o = open(o, 'rb').read()
    if isinstance(o, bytes):
        return io.BytesIO(o)
    if isinstance(o, str):
        return io.StringIO(o)
    raise TypeError(f"bad input: {o!r}")

def mode(o, mode):
    if not hasattr(o, 'mode'):
        raise TypeError(f"input has no mode attribute: {o}")
    if o.mode == mode:
        return o
    return os.fdopen(o.fileno(), mode)

