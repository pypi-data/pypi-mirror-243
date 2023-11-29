from simpleuid import alpha, alphanumeric

def test_alphanumeric():
    assert alphanumeric().isalnum() == True

def test_alphanumeric_length():
    assert len(alphanumeric()) == 10
    assert len(alphanumeric(length=200)) == 200

def test_alphanumeric_prefix():
    assert alphanumeric(prefix="test")[:4] == "test"

def test_alpha_case():
    assert alphanumeric(case="upper").isupper() == True
    assert alphanumeric(case="lower").islower() == True
    
    allcase = alphanumeric()
    assert (allcase.isupper() == False and allcase.islower() == False) == True
