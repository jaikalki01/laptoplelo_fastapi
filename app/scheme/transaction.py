from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionBase(BaseModel):
    user_id: int
    transaction_id: str
    type: str
    method: str
    amount: float
    status: str

class TransactionCreate(TransactionBase):
    pass
class TransactionOut(BaseModel):
    id: int
    transaction_id: str
    user_id: int
    type: str
    method: str
    amount: float
    status: str
    created_at: datetime

    user_name: Optional[str] = None
    user_email: Optional[str] = None
    user_phone: Optional[str] = None

    class Config:
        orm_mode = True
