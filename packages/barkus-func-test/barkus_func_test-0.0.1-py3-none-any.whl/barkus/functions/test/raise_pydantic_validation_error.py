from pydantic import BaseModel

class Something(BaseModel):
    value: int

def raise_validation_error(*args, **kwargs):
    from typing import Any
    value: Any = "batata"
    Something(value = value)