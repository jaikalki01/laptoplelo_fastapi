# app/scheme/coupon.py
from pydantic import BaseModel
from enum import Enum

class CouponType(str, Enum):
    percentage = "percentage"
    flat = "flat"

class CouponBase(BaseModel):
    code: str
    discount_type: CouponType
    discount_value: float
    min_cart_value: float = 0
    is_active: int = 1

class CouponCreate(CouponBase):
    pass

class CouponOut(CouponBase):
    id: int

    class Config:
        from_attributes = True
