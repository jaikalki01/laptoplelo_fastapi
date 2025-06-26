from sqlalchemy import Column, String, Float, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.id"))
    product_id = Column(String, ForeignKey("products.id"))
    date = Column(DateTime, default=datetime.utcnow)
    rent_duration = Column(Integer, default=30)
    total = Column(Float)
    status = Column(String, default="pending")
    type = Column(String, default="rent")

    user = relationship("User", back_populates="rentals")
    product = relationship("Product", back_populates="rentals")
