import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import User
from app.models.transaction import Transaction
from app.scheme.transaction import TransactionCreate, TransactionOut
from app.crud import transaction as crud

router = APIRouter(prefix="/api/v1/transaction", tags=["Transaction"])

@router.post("/create", response_model=TransactionOut)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_txn = Transaction(
        transaction_id=f"TXN-{uuid.uuid4().hex[:10].upper()}",
        user_id=transaction.user_id,
        type=transaction.type,
        method=transaction.method,
        amount=transaction.amount,
        status=transaction.status
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)

    return {
        "id": new_txn.id,
        "transaction_id": new_txn.transaction_id,
        "user_id": new_txn.user_id,
        "type": new_txn.type,
        "method": new_txn.method,
        "amount": new_txn.amount,
        "status": new_txn.status,
        "created_at": new_txn.created_at,
        "user_name": user.name,
        "user_email": user.email,
        "user_phone": user.phone,
    }


@router.get("/list", response_model=list[TransactionOut])
def list_transactions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_transactions(db, skip, limit)
