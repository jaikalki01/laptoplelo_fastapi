from sqlalchemy import Column, String, Float, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from datetime import date
from app.database import Base

class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, autoincrement=True)

    # FIXED line below:
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    rent_duration = Column(Integer, default=30)
    total = Column(Float)
    status = Column(String(20), default="pending")
    date = Column(Date, default=date.today)

    user = relationship("User", back_populates="rentals")
