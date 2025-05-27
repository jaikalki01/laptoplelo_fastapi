# app/crud/coupon.py
from sqlalchemy.orm import Session
from app.models.coupon import Coupon
from app.scheme.coupon import CouponCreate

def create_coupon(db: Session, coupon: CouponCreate):
    db_coupon = Coupon(**coupon.dict())
    db.add(db_coupon)
    db.commit()
    db.refresh(db_coupon)
    return db_coupon

def get_coupon_by_code(db: Session, code: str):
    return db.query(Coupon).filter(Coupon.code == code, Coupon.is_active == 1).first()

# app/crud/coupon.py
def get_all_coupons(db: Session):
    return db.query(Coupon).all()


def deactivate_coupon(db: Session, coupon_id: int):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        db_coupon.is_active = 0  # Deactivate coupon
        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    return None

def activate_coupon(db: Session, coupon_id: int):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        db_coupon.is_active = 1  # Deactivate coupon
        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    return None

# app/crud/coupon.py
def delete_coupon(db: Session, coupon_id: int):
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        db.delete(db_coupon)
        db.commit()
        return db_coupon
    return None
