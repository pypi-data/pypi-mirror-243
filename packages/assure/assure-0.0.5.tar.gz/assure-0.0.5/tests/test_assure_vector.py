import numpy as np
from assure import vector
from assure import vectors
from assure import harmonize

def test_vector():
    a = np.arange(1024)
    b = np.arange(1024).reshape((1, -1))
    c = np.arange(2048).reshape((2, -1))
    assert vector(a).shape == (1024,)
    assert vector(b).shape == (1024,)
    assert np.allclose(vector(a), vector(b))
    try:
        vector(c)
    except TypeError:
        pass
    else:
        raise Exception

def test_vectors():
    a = np.arange(1024)
    b = a[None, ...]
    c = b[None, ...]

    assert vectors(a).shape == (1, 1024)

    assert vectors(b).shape == (1, 1024)

    try:
        vectors(c).shape
    except TypeError:
        pass
    else:
        raise Exception

    assert vectors([a,b]).shape == (2, 1024)

    assert vectors([vectors(a), a, b, vectors(b)]).shape == (4, 1024)

    # dict_values
    d = {'a': np.arange(5), 'b': np.arange(5)}
    assert vectors(d.values()).shape == (2,5)


def test_harmonize():
    a = np.arange(1024)
    b = np.arange(2048)
    c = np.arange(4096)
    d = np.arange(4097)

    assert [x.shape for x in harmonize(a,b,c)] \
        == [(1, 1024), (2, 1024), (4, 1024)]

    try:
        [x.shape for x in harmonize(a,b,c,d)]
    except ValueError:
        pass
    else:
        raise Exception
