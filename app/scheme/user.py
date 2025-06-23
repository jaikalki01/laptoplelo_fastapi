# scheme/user.py
from pydantic import BaseModel
from typing import List
from app.scheme.address import Address  # Import Address from the new address scheme

class UserBase(BaseModel):
    name: str
    email: str
    role: str
    kyc_verified: bool
    password: str
class UserCreate(UserBase):
    password: str

class LoginForm(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(UserBase):
    id: int
    addresses: List[Address]  # This is now just referring to the Address model
    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
