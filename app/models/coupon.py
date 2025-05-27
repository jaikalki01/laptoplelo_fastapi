# app/models/coupon.py
from sqlalchemy import Column, Integer, String, Float, Enum
from app.database import Base
import enum

class CouponType(str, enum.Enum):
    percentage = "percentage"
    flat = "flat"

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(200), unique=True, nullable=False)
    discount_type = Column(Enum(CouponType), nullable=False)
    discount_value = Column(Float, nullable=False)
    min_cart_value = Column(Float, default=0.0)  # optional
    is_active = Column(Integer, default=1)  # 1 for active, 0 for inactive
