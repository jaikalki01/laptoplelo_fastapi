from sqlalchemy import Column, Integer, String, Boolean, Enum, Float
from app.database import Base

class Coupon(Base):
    __tablename__ = "coupons"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, nullable=False)
    discount_type = Column(String, nullable=False)  # "percentage" or "fixed"
    discount_value = Column(Float, nullable=False)
    is_active = Column(Boolean, default=True)
