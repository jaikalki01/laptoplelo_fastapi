from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import String

class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    rental_duration = Column(Integer, default=30)
    type = Column(String(10))  # "rental" or "sale"

    product = relationship("Product")
