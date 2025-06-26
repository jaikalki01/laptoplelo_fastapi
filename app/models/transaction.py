from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(String(100), unique=True, index=True)  # ✅ Length added
    user_id = Column(Integer, ForeignKey("users.id"))
    type = Column(String(50))     # ✅ Length added
    method = Column(String(50))   # ✅ Length added
    amount = Column(Float)
    status = Column(String(50))   # ✅ Length added
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

