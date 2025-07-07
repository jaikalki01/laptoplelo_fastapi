from sqlalchemy import Column, String, Integer, Boolean, Float, JSON
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.ext.mutable import MutableList
class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))
    description = Column(String(1000))
    price = Column(Float)
    rental_price = Column(Float)
    type = Column(String(50))  # 'sale' or 'rent'
    brand = Column(String(255))
    image = Column(String(255))  # cover image
    images = Column(MutableList.as_mutable(JSON), default=list, nullable=False)
    specs = Column(JSON)
    available = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)

    wishlists = relationship("Wishlist", back_populates="product")
    rentals = relationship("Rental", back_populates="product", cascade="all, delete-orphan")