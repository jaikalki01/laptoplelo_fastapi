from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, scheme
from app.database import SessionLocal
from app.crud.wishlist import add_to_wishlist, remove_from_wishlist, get_user_wishlist
from app.auth.jwt_handler import verify_user_token
from app.models.wishlist import Wishlist

router = APIRouter()


def get_db():
    db = SessionLocal()  # Assuming SessionLocal is defined somewhere
    try:
        yield db
    finally:
        db.close()


@router.post("/wishlist/{product_id}")
def add_to_user_wishlist(product_id: int, db: Session = Depends(get_db),
                         user_id: int = Depends(verify_user_token)):
    wishlist_item = add_to_wishlist(db, user_id, product_id)
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product added to wishlist", "wishlist_item": wishlist_item}


@router.delete("/wishlist/{product_id}")
def remove_from_user_wishlist(product_id: int, db: Session = Depends(get_db),
                              user_id: int = Depends(verify_user_token)):
    wishlist_item = remove_from_wishlist(db, user_id, product_id)
    if wishlist_item is None:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    return {"message": "Product removed from wishlist", "wishlist_item": wishlist_item}


@router.get("/wishlist")
def get_user_wishlist_items(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_user_token)  # directly get user_id from token
):
    wishlist = get_user_wishlist(db, user_id)
    return {"wishlist": wishlist}

@router.get("/wishlist/count")
def get_wishlist_count(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_user_token)
):
    wishlist_count = db.query(Wishlist).filter(Wishlist.user_id == user_id).count()
    return {"total_wishlist_items": wishlist_count}




