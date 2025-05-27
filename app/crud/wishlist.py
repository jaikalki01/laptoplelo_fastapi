from sqlalchemy.orm import Session
from app.models import Wishlist, Product, User



def add_to_wishlist(db: Session, user_id: int, product_id: int):
    # Check if product exists
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        return None

    # Check if product is already in the wishlist
    existing_wishlist = db.query(Wishlist).filter(
        Wishlist.user_id == user_id, Wishlist.product_id == product_id
    ).first()
    if existing_wishlist:
        return existing_wishlist  # Already added

    wishlist_item = Wishlist(user_id=user_id, product_id=product_id)
    db.add(wishlist_item)
    db.commit()
    db.refresh(wishlist_item)
    return wishlist_item


def remove_from_wishlist(db: Session, user_id: int, product_id: int):
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id, Wishlist.product_id == product_id
    ).first()

    if wishlist_item:
        db.delete(wishlist_item)
        db.commit()
        return wishlist_item
    return None


def get_user_wishlist(db: Session, user_id: int):
    return db.query(Product).join(Wishlist).filter(Wishlist.user_id == user_id).all()
