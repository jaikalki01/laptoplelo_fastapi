from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import Dict

from app.crud import cart as cart_crud
from app.scheme.cart import CartCreate, CartRemoveSchema
from app.database import SessionLocal
from app.auth.jwt_handler import verify_user_token
from app.models.cart import Cart

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
    user_id: int = Depends(verify_user_token),
    db: Session = Depends(get_db)
):
    return cart_crud.create_cart_item(db, item, user_id=user_id)

@router.post("/remove")
def remove_cart_item(
    payload: CartRemoveSchema,
    user_id: int = Depends(verify_user_token),
    db: Session = Depends(get_db),
) -> Dict[str, str]:
    try:
        return cart_crud.remove_from_cart(
            db=db,
            product_id=payload.product_id,
            user_id=user_id,
            item_type=payload.type  # Changed parameter name here
        )
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to remove item: {str(e)}"
        )

@router.get("/")
def get_cart(
    user_id: int = Depends(verify_user_token),
    db: Session = Depends(get_db)
):
    return cart_crud.get_cart_items_by_user(db, user_id)

@router.get("/count")
def get_cart_count(
    user_id: int = Depends(verify_user_token),
    db: Session = Depends(get_db)
) -> Dict[str, int]:
    total_quantity = db.query(func.sum(Cart.quantity)).filter(
        Cart.user_id == user_id
    ).scalar() or 0
    return {"total_cart_items": int(total_quantity)}

@router.delete("/clear")
def clear_cart(
    user_id: int = Depends(verify_user_token),
    db: Session = Depends(get_db)
) -> Dict[str, str]:
    try:
        cart_crud.clear_cart(db, user_id)
        return {"message": "Cart cleared successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to clear cart: {str(e)}"
        )
