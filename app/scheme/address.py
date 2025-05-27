from pydantic import BaseModel
from typing import Optional

class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    pincode: str
    is_default: bool

class AddressCreate(AddressBase):
    pass

class Address(AddressBase):
    id: int
    class Config:
        from_attributes = True
