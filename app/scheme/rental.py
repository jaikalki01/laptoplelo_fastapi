from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True

class ProductBase(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

# ✅ This should be a TOP-LEVEL class
class RentalCreate(BaseModel):
    user_id: int
    product_id: int
    date: datetime
    rent_duration: int
    total: float
    status: str
    type: Optional[str] = "rent"

    class Config:
        orm_mode = True

class RentalOut(BaseModel):
    id: str
    user_id: int
    product_id: int
    date: datetime
    rent_duration: int
    total: float
    status: str
    type: Optional[str]
    user: UserBase
    product: ProductBase

    class Config:
        orm_mode = True
