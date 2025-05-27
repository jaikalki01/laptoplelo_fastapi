from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Address(Base):
    __tablename__ = "addresses"
    id = Column(Integer, primary_key=True, index=True)
    street = Column(String(255))
    city = Column(String(100))
    state = Column(String(100))
    pincode = Column(String(10))
    is_default = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="addresses")
