from simpleuid import alpha

def test_alpha():
    assert alpha().isalpha() == True

def test_alpha_length():
    assert len(alpha()) == 10
    assert len(alpha(length=200)) == 200

def test_alpha_prefix():
    assert alpha(prefix="test")[:4] == "test"

def test_alpha_case():
    assert alpha(case="upper").isupper() == True
    assert alpha(case="lower").islower() == True
    
    allcase = alpha()
    assert (allcase.isupper() == False and allcase.islower() == False) == True
