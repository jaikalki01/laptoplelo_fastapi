from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.scheme.coupon import CouponOut, CouponCreate
from app.crud import coupon as crud_coupon
from app.database import SessionLocal
from app.auth.jwt_handler import verify_admin_token

router = APIRouter(prefix="/coupon", tags=["Coupons"])  # Changed tag to plural for consistency

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Coupon - Fixed endpoint path (removed duplicate /coupon)
@router.post(
    "/",
    response_model=CouponOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new coupon",
    description="Admin-only endpoint to create new discount coupons"
)
def create_coupon(
    coupon: CouponCreate, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_admin_token)
):
    # Check if coupon code already exists
    existing_coupon = crud_coupon.get_coupon_by_code(db, code=coupon.code)
    if existing_coupon:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Coupon code already exists"
        )
    return crud_coupon.create_coupon(db, coupon)

# Get All Coupons
@router.get(
    "/",
    response_model=List[CouponOut],
    summary="Get all coupons",
    description="Retrieve a list of all available coupons"
)
def get_all_coupons(db: Session = Depends(get_db)):
    return crud_coupon.get_all_coupons(db)

# Validate Coupon
@router.get(
    "/validate/{code}",
    response_model=CouponOut,
    summary="Validate a coupon",
    description="Check if a coupon is valid for a given cart total"
)
def validate_coupon(
    code: str, 
    total: float, 
    db: Session = Depends(get_db)
):
    coupon = crud_coupon.get_coupon_by_code(db, code)
    if not coupon or not coupon.is_active:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid or expired coupon"
        )
    if coupon.min_cart_value and total < coupon.min_cart_value:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Cart value must be at least {coupon.min_cart_value} for this coupon"
        )
    return coupon

# Coupon Status Management
@router.patch(
    "/{coupon_id}/deactivate",
    response_model=CouponOut,
    summary="Deactivate a coupon",
    description="Admin-only endpoint to deactivate a coupon"
)
def deactivate_coupon(
    coupon_id: int, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_admin_token)
):
    coupon = crud_coupon.deactivate_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    return coupon

@router.patch(
    "/{coupon_id}/activate",
    response_model=CouponOut,
    summary="Activate a coupon",
    description="Admin-only endpoint to activate a coupon"
)
def activate_coupon(
    coupon_id: int, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_admin_token)
):
    coupon = crud_coupon.activate_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    return coupon

# Delete Coupon
@router.delete(
    "/{coupon_id}",
    response_model=CouponOut,
    summary="Delete a coupon",
    description="Admin-only endpoint to permanently delete a coupon"
)
def delete_coupon(
    coupon_id: int, 
    db: Session = Depends(get_db), 
    token: str = Depends(verify_admin_token)
):
    coupon = crud_coupon.delete_coupon(db, coupon_id)
    if not coupon:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coupon not found"
        )
    return coupon