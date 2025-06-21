from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.models.coupon import Coupon
from app.scheme.coupon import CouponCreate, CouponUpdate
from fastapi import HTTPException, status

def create_coupon(db: Session, coupon: CouponCreate) -> Coupon:
    """
    Create a new coupon in the database
    Args:
        db: Database session
        coupon: Coupon data to create
    Returns:
        Coupon: The created coupon
    Raises:
        HTTPException: If coupon code already exists
    """
    try:
        db_coupon = Coupon(
            code=coupon.code.upper().strip(),  # Normalize coupon code
            discount_type=coupon.discount_type,
            discount_value=coupon.discount_value,
            min_cart_value=coupon.min_cart_value,
            is_active=True  # Default to active when created
        )
        db.add(db_coupon)
        db.commit()
        db.refresh(db_coupon)
        return db_coupon
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon code already exists"
        )

def get_coupon_by_code(db: Session, code: str, active_only: bool = True) -> Coupon | None:
    """
    Get a coupon by its code
    Args:
        db: Database session
        code: Coupon code to search for
        active_only: Whether to only return active coupons
    Returns:
        Coupon: The found coupon or None
    """
    query = db.query(Coupon).filter(Coupon.code == code.upper().strip())
    if active_only:
        query = query.filter(Coupon.is_active == True)
    return query.first()

def get_all_coupons(db: Session, active_only: bool = False) -> list[Coupon]:
    """
    Get all coupons from the database
    Args:
        db: Database session
        active_only: Whether to only return active coupons
    Returns:
        list[Coupon]: List of coupons
    """
    query = db.query(Coupon)
    if active_only:
        query = query.filter(Coupon.is_active == True)
    return query.all()

def update_coupon(db: Session, coupon_id: int, coupon_data: CouponUpdate) -> Coupon | None:
    """
    Update coupon details
    Args:
        db: Database session
        coupon_id: ID of coupon to update
        coupon_data: Data to update
    Returns:
        Coupon: The updated coupon or None if not found
    """
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        for key, value in coupon_data.dict(exclude_unset=True).items():
            setattr(db_coupon, key, value)
        db.commit()
        db.refresh(db_coupon)
    return db_coupon

def toggle_coupon_status(db: Session, coupon_id: int, active: bool) -> Coupon | None:
    """
    Toggle coupon active status
    Args:
        db: Database session
        coupon_id: ID of coupon to update
        active: New status (True/False)
    Returns:
        Coupon: The updated coupon or None if not found
    """
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        db_coupon.is_active = active
        db.commit()
        db.refresh(db_coupon)
    return db_coupon

def activate_coupon(db: Session, coupon_id: int):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if coupon:
        coupon.is_active = True  # Use boolean True/False
        db.commit()
        db.refresh(coupon)
    return coupon

def deactivate_coupon(db: Session, coupon_id: int):
    coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if coupon:
        coupon.is_active = False  # Use boolean True/False
        db.commit()
        db.refresh(coupon)
    return coupon

def delete_coupon(db: Session, coupon_id: int) -> Coupon | None:
    """
    Permanently delete a coupon
    Args:
        db: Database session
        coupon_id: ID of coupon to delete
    Returns:
        Coupon: The deleted coupon or None if not found
    """
    db_coupon = db.query(Coupon).filter(Coupon.id == coupon_id).first()
    if db_coupon:
        db.delete(db_coupon)
        db.commit()
    return db_coupon