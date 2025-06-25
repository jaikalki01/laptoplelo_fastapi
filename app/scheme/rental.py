from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

from app.database import Session, SessionLocal


class RentalBase(BaseModel):
    user_id: int  # ✅ FIXED
    rent_duration: int = 30
    total: float
    status: str = "pending"

class RentalCreate(RentalBase):
    pass

class RentalUpdate(BaseModel):
    status: str

class RentalOut(RentalBase):
    id: int  # ✅ Should match your SQLAlchemy model
    date: datetime
    class Config:
        from_attributes = True


def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
