from .simpleuid import *
from typing import Optional
from .types import Case

def alpha(length:int  = 10, prefix: Optional[str] = "", case: Optional[Case] = "all"):
    return simpleuid.alpha(length, prefix, case)

def alphanumeric(length:int = 10, prefix: Optional[str] = "", case: Optional[Case] = "all"):
    return simpleuid.alphanumeric(length, prefix, case)

def numeric(length:int = 10, prefix: Optional[str] = ""):
    return simpleuid.numeric(length, prefix)

def var(varstring: str, prefix: Optional[str] = ""):
    return simpleuid.var(varstring, prefix)
