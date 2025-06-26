from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserOut(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None  # ✅ Allow phone to be nullable

    class Config:
        orm_mode = True

class ProductOut(BaseModel):
    id: int
    name: str
    price: float

    class Config:
        orm_mode = True

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
    id: int
    user_id: Optional[int] = None  # ✅ if this can be null
    product_id: Optional[int] = None
    date: datetime
    rent_duration: int
    total: float
    status: str
    type: Optional[str] = None

    product: Optional[ProductOut] = None
    user: Optional[UserOut] = None

    class Config:
        orm_mode = True
