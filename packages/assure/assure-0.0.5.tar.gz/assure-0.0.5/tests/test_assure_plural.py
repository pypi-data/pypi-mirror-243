import assure

def test_assure_plural():
    n = 42
    l = [n]
    assert assure.singular(l) == n
    assert assure.singular(n) == n
    assert assure.plural(n) == l
    assert assure.plural(l) == l
    assert assure.plural({n}) == {n}
    assert assure.plural((n,l)) == (n,l)

