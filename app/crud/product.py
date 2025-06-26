from sqlalchemy.orm import Session
from app.models.product import Product
from app.scheme.product import ProductCreate, ProductUpdate

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Product).offset(skip).limit(limit).all()

def get_product(db: Session, product_id: str):
    return db.query(Product).filter(Product.id == product_id).first()


def create_product(db: Session, product: ProductCreate):
    db_product = Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def update_product(db: Session, product_id: str, updated_data: dict):
    product = get_product(db, product_id)
    if product:
        # Convert updated_data to dictionary if it's a Pydantic model
        updated_data = updated_data.dict(exclude_unset=True) if hasattr(updated_data, 'dict') else updated_data

        for key, value in updated_data.items():
            setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product


def delete_product(db: Session, product_id: str):
    product = get_product(db, product_id)
    if product:
        db.delete(product)
        db.commit()
    return product
