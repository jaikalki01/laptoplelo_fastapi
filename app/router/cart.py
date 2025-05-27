from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud import cart as cart_crud
from app.scheme.cart import CartCreate
from app.database import SessionLocal
from app.crud.cart import remove_from_cart
from app.scheme.cart import CartRemoveSchema
from app.auth.jwt_handler import verify_user_token
from app.models.cart import Cart
from sqlalchemy import func

router = APIRouter(prefix="/cart", tags=["Cart"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def add_to_cart(
    item: CartCreate,
    user_id: int = Depends(verify_user_token),  # <-- Require user token
    db: Session = Depends(get_db)
):
    # You have the user_id now, pass it if needed to create_cart_item
    return cart_crud.create_cart_item(db, item, user_id=user_id)

@router.post("/cart/remove")
def remove_cart_item(
    payload: CartRemoveSchema,
    user_id: int = Depends(verify_user_token),  # get user_id from token
    db: Session = Depends(get_db),
):
    return remove_from_cart(
        db=db,
        product_id=payload.product_id,
        user_id=user_id,  # use user_id from token, not payload
        type=payload.type,
    )


@router.get("/")
def get_cart(
    user_id: int = Depends(verify_user_token),  # <-- Require user token
    db: Session = Depends(get_db)
):
    return cart_crud.get_cart_items_by_user(db, user_id)

@router.get("/cart/count")
def get_cart_count(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_user_token)
):
    total_quantity = db.query(func.sum(Cart.quantity)).filter(Cart.user_id == user_id).scalar() or 0
    return {"total_cart_items": total_quantity}
