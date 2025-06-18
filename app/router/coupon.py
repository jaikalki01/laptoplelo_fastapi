# app/router/coupon.py
from typing import List
from app.auth.jwt_handler import verify_admin_token
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.scheme.coupon import CouponOut, CouponCreate
from app.crud import coupon as crud_coupon
from app.database import SessionLocal


router = APIRouter(prefix="/coupon", tags=["Coupon"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/coupon", response_model=CouponOut)
def create_coupon(coupon: CouponCreate, db: Session = Depends(get_db), token: str = Depends(verify_admin_token)):
    return crud_coupon.create_coupon(db, coupon)

@router.get("/{code}", response_model=CouponOut)
def validate_coupon(code: str, total: float, db: Session = Depends(get_db)):
    coupon = crud_coupon.get_coupon_by_code(db, code)
    if not coupon:
        raise HTTPException(status_code=404, detail="Invalid or expired coupon")
    if total < coupon.min_cart_value:
        raise HTTPException(status_code=400, detail="Cart value too low for this coupon")
    return coupon

# app/router/coupon.py
@router.get("/", response_model=List[CouponOut])
def get_all_coupons(db: Session = Depends(get_db)):
    coupons = crud_coupon.get_all_coupons(db)
    return coupons


# app/router/coupon.py
@router.delete("/deactivate/{coupon_id}", response_model=CouponOut)
def deactivate_coupon(coupon_id: int, db: Session = Depends(get_db), token: str = Depends(verify_admin_token)):
    coupon = crud_coupon.deactivate_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

# app/router/coupon.py
@router.post("/activate/{coupon_id}", response_model=CouponOut)
def activate_coupon(coupon_id: int, db: Session = Depends(get_db), token: str = Depends(verify_admin_token)):
    coupon = crud_coupon.activate_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon

# app/router/coupon.py
@router.delete("/delete/{coupon_id}", response_model=CouponOut)
def delete_coupon(coupon_id: int, db: Session = Depends(get_db), token: str = Depends(verify_admin_token)):
    coupon = crud_coupon.delete_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(status_code=404, detail="Coupon not found")
    return coupon
