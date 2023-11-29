#!/usr/bin/env python3

__all__ = [
    'bytes',
]

import os
import builtins

def bytes(arg):
    if isinstance(arg, builtins.bytes):
        return arg
    if hasattr(arg, 'read'):
        arg = arg.read()
    elif os.path.exists(arg):
        arg = open(arg, 'rb').read()
    if isinstance(arg, str):
        arg = arg.encode()
    if isinstance(arg, builtins.bytes):
        return arg
    cls = type(arg)
    raise FileNotFoundError(f"Could not cast to bytes: {cls.__name__!r}")
