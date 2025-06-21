from sqlalchemy.orm import Session
from app.models.cart import Cart
from app.scheme.cart import CartCreate
from fastapi import HTTPException, status
from typing import List, Optional


def create_cart_item(db: Session, item: CartCreate, user_id: int) -> Cart:
    """
    Creates or updates a cart item for a user.

    Args:
        db: Database session
        item: Cart item data
        user_id: ID of the user owning the cart

    Returns:
        The created or updated cart item

    Raises:
        HTTPException: If there's a validation error
    """
    try:
        item_data = item.dict()
        item_data['user_id'] = user_id

        # Check for existing item
        existing_item = db.query(Cart).filter_by(
            product_id=item_data['product_id'],
            user_id=user_id,
            type=item_data['type']
        ).first()

        if existing_item:
            # Update existing item
            existing_item.quantity = item_data['quantity']
            if 'rental_duration' in item_data:
                existing_item.rental_duration = item_data['rental_duration']
            db.commit()
            db.refresh(existing_item)
            return existing_item

        # Create new item
        db_item = Cart(**item_data)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update cart: {str(e)}"
        )


def remove_from_cart(db: Session, product_id: int, user_id: int, item_type: str) -> dict:
    """
    Removes a specific item from the user's cart.

    Args:
        db: Database session
        product_id: ID of the product to remove
        user_id: ID of the user owning the cart
        item_type: Type of the item ('sale' or 'rent')

    Returns:
        Success message

    Raises:
        HTTPException: If item not found
    """
    try:
        cart_item = db.query(Cart).filter(
            Cart.product_id == product_id,
            Cart.user_id == user_id,
            Cart.type == item_type
        ).first()

        if not cart_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Cart item not found"
            )

        db.delete(cart_item)
        db.commit()
        return {"message": "Item removed successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to remove item: {str(e)}"
        )


def get_cart_items_by_user(db: Session, user_id: int) -> List[Cart]:
    """
    Retrieves all cart items for a specific user.

    Args:
        db: Database session
        user_id: ID of the user

    Returns:
        List of cart items
    """
    return db.query(Cart).filter(Cart.user_id == user_id).all()