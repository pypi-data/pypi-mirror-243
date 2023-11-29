from simpleuid import numeric

def test_numeric():
    assert numeric().isdigit() == True

def test_numeric_length():
    assert len(numeric()) == 10
    assert len(numeric(length=200)) == 200
    assert len(numeric(length=200, prefix="test")) == 204

def test_numeric_prefix():
    assert numeric(prefix="test")[:4] == "test"
