import uuid

from sqlalchemy.orm import Session
from app.models.transaction import Transaction
from app.models.user import User
from app.scheme.transaction import TransactionCreate
from typing import List
from datetime import datetime

def create_transaction(db: Session, transaction: TransactionCreate):
    new_txn = Transaction(
        transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
        user_id=transaction.user_id,
        type=transaction.type,
        method=transaction.method,
        amount=transaction.amount,
        status=transaction.status,
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

def get_transactions(db: Session, skip: int = 0, limit: int = 100):
    txns = db.query(Transaction).offset(skip).limit(limit).all()
    result = []
    for t in txns:
        result.append({
            "id": t.id,
            "transaction_id": t.transaction_id,
            "user_id": t.user_id,
            "type": t.type,
            "method": t.method,
            "amount": t.amount,
            "status": t.status,
            "created_at": t.created_at,
            "user_name": t.user.name if t.user else None,
            "user_email": t.user.email if t.user else None,
            "user_phone": t.user.phone if t.user else None,
        })
    return result

