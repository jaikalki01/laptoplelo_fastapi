from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.transaction import Transaction
from app.models.user import User
from datetime import datetime
from collections import defaultdict

router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.get("/overview")
def get_analytics_overview(db: Session = Depends(get_db)):
    total_users = db.query(User).count()
    kyc_verified = db.query(User).filter(User.kyc_verified == True).count()

    transactions = db.query(Transaction).all()
    completed = [t for t in transactions if t.status == "completed"]
    total_revenue = sum(t.amount for t in completed)
    total_sales = sum(1 for t in completed if t.type == "sale")
    total_rentals = sum(1 for t in completed if t.type == "rent")

    return {
        "total_users": total_users,
        "kyc_verified": kyc_verified,
        "total_revenue": total_revenue,
        "total_sales": total_sales,
        "total_rentals": total_rentals,
    }


@router.get("/monthly-revenue")
def get_monthly_revenue(db: Session = Depends(get_db)):
    data = defaultdict(lambda: {"sales": 0, "rentals": 0})
    transactions = db.query(Transaction).filter(Transaction.status == "completed").all()

    for t in transactions:
        month = t.created_at.strftime("%b")
        if t.type == "sale":
            data[month]["sales"] += t.amount
        elif t.type == "rent":
            data[month]["rentals"] += t.amount

    return [{"month": k, **v} for k, v in sorted(data.items())]
