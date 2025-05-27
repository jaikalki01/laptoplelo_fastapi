from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.scheme.cart import CartCreate
from fastapi import HTTPException

def create_cart_item(db: Session, item: CartCreate, user_id: int):
    # Inject user_id into the item data dict
    item_data = item.dict()
    item_data['user_id'] = user_id

    existing_item = db.query(Cart).filter_by(
        product_id=item_data['product_id'],
        user_id=user_id,            # use user_id here directly
        type=item_data['type'],
    ).first()

    if existing_item:
        # Update the quantity
        existing_item.quantity = item_data['quantity']
        existing_item.rental_duration = item_data.get('rental_duration')
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        # Create new item with user_id injected
        db_item = Cart(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item



def remove_from_cart(db: Session, product_id: str, user_id: int, type: str):
    cart_items = db.query(Cart).filter(
        Cart.product_id == product_id,
        Cart.user_id == user_id
    ).all()

    if not cart_items:
        raise HTTPException(status_code=404, detail="No cart items found for this product")

    for item in cart_items:
        db.delete(item)

    db.commit()
    return {"message": "Item removed"}

def get_cart_items_by_user(db: Session, user_id: int):
    cart_items = db.query(Cart).filter(Cart.user_id == user_id).all()
    return cart_items
