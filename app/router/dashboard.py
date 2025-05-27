from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.scheme.dashboard import DashboardStats
from app.crud.dashboard import get_dashboard_stats
from app.auth.jwt_handler import verify_admin_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/stats", response_model=DashboardStats)
def read_dashboard_stats(db: Session = Depends(get_db), token: str = Depends(verify_admin_token)):
    return get_dashboard_stats(db)
