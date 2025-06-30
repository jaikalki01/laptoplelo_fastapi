# app/scheme/user.py

from pydantic import BaseModel
from typing import List
from app.scheme.address import Address  # Ensure this exists

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str
    kyc_verified: bool

class LoginForm(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class User(BaseModel):
    id: int
    name: str
    email: str
    role: str
    kyc_verified: bool
    addresses: List[Address]

    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
