import os
import sys
import assure

class make_stream:
    def __init__(self, mode):
        self.pipe = os.popen("echo hello world")
        self.mode = mode
    def __enter__(self):
        self.file = os.fdopen(self.pipe.fileno(), self.mode)
        return self.file
    def __exit__(self, et, ev, tb):
        self.file.close()

def test_assure_stream():

    with make_stream('r') as stream:
        assert not stream.seekable()

    with make_stream('r') as stream:
        assert assure.seekable(stream).seekable()

    with make_stream('rb') as stream:
        assert not stream.seekable()

    with make_stream('rb') as stream:
        assert assure.seekable(stream).seekable()

    assert assure.seekable(b'hello world').seekable()
