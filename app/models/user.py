from sqlalchemy import Column, String, Boolean, Integer
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255),nullable=False)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255),nullable=False)
    role = Column(String(50),default="user")
    kyc_verified = Column(Boolean, default=False)

    addresses = relationship("Address", back_populates="user", cascade="all, delete-orphan")
    wishlists = relationship("Wishlist", back_populates="user",cascade="all, delete-orphan")
    rentals = relationship("Rental", back_populates="user")