import io
import assure
import pathlib
import tempfile

def test_assure_bytes():
    path = tempfile.mktemp()
    with open(path, 'w') as fp:
        fp.write("Hello world\n")

    from_file_rs = assure.bytes(open(path, 'r'))
    assert isinstance(from_file_rs, bytes)

    from_file_rb = assure.bytes(open(path, 'rb'))
    assert isinstance(from_file_rb, bytes)

    from_pathlib = assure.bytes(pathlib.Path(path))
    assert isinstance(from_pathlib, bytes)

    from_path = assure.bytes(path)
    assert isinstance(from_path, bytes)

    from_string_io = assure.bytes(io.StringIO(open(path, 'r').read()))
    assert isinstance(from_string_io, bytes)

    from_bytes_io = assure.bytes(io.BytesIO(open(path, 'rb').read()))
    assert isinstance(from_bytes_io, bytes)

    from_string = assure.bytes(open(path, 'r').read())
    assert isinstance(from_string, bytes)

    from_bytes = assure.bytes(open(path, 'rb').read())
    assert isinstance(from_bytes, bytes)

