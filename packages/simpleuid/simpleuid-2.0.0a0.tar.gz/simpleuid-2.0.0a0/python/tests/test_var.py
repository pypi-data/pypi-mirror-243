from simpleuid import var
from datetime import datetime

def test_variables():
    today = datetime.today()
    year = str(today.year)
    year_short = str(today.year)[-2:]
    
    assert var("%yyyy") == year
    assert var("%yy") == year_short

def test_alpha_prefix():
    assert var("%yyyy", prefix="test")[:4] == "test"
