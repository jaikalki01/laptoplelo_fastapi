from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    phone: str
    message: str


class ContactOut(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    message: str
    created_at: datetime


    class Config:
        from_attributes = True