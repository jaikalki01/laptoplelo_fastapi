from sqlalchemy import Column, String, Integer, Boolean, Float, JSON
from app.database import Base
from sqlalchemy.orm import relationship

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    description = Column(String(100))
    price = Column(Float)
    rental_price = Column(Float)
    type = Column(String(100))
    image = Column(String(100))
    brand = Column(String(100))
    specs = Column(JSON)
    available = Column(Boolean, default=True)
    featured = Column(Boolean, default=False)

    wishlists = relationship("Wishlist", back_populates="product")
