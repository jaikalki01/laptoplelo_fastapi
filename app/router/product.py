from operator import or_

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Product
from app.scheme.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud
import os
from datetime import datetime
from fastapi.responses import JSONResponse
from app.auth.jwt_handler import verify_admin_token
from typing import List, Optional
import uuid
import aiofiles
from app.models.cart import Cart
from pydantic import BaseModel

router = APIRouter(prefix="/products", tags=["Products"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


UPLOAD_DIR = "static/uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)


class ProductSpecs(BaseModel):
    processor: str
    ram: str
    storage: str
    display: Optional[str] = None
    graphics: Optional[str] = None


@router.get("/", response_model=List[ProductOut])
def list_products(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(Product)
    if search:
        query = query.filter(
            or_(
                Product.name.ilike(f"%{search}%"),
                Product.description.ilike(f"%{search}%"),
                Product.brand.ilike(f"%{search}%")
            )
        )
    return query.all()


@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: str, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
async def create_product(
        name: str = Form(...),
        description: str = Form(...),
        price: float = Form(...),
        rental_price: float = Form(...),
        type: str = Form(...),
        brand: str = Form(...),
        processor: str = Form(...),
        ram: str = Form(...),  # Changed from memory to ram
        storage: str = Form(...),
        display: str = Form(None),
        graphics: str = Form(None),
        availability: bool = Form(True),  # Changed from available to availability
        featured: bool = Form(False),
        images: List[UploadFile] = File(...),
        db: Session = Depends(get_db),
        user: dict = Depends(verify_admin_token)
):
    # Validate at least one image
    if not images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image is required"
        )

    # Validate not more than 4 images
    if len(images) > 4:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 4 images allowed"
        )

    # Save images
    saved_images = []
    for img in images:
        ext = os.path.splitext(img.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        async with aiofiles.open(filepath, "wb") as f:
            content = await img.read()
            await f.write(content)

        saved_images.append(filename)

    # Create product data
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "rental_price": rental_price,
        "type": type,
        "brand": brand,
        "image": saved_images[0],  # First image as main image
        "available": availability,  # Map to available in DB
        "featured": featured,
        "specs": {
            "processor": processor,
            "memory": ram,  # Map ram to memory in DB
            "storage": storage,
            "display": display,
            "graphics": graphics
        },
        "images": saved_images  # Store all images
    }

    product_schema = ProductCreate(**product_data)
    product = crud.create_product(db, product_schema)

    # Rename files with product ID
    final_images = []
    for idx, filename in enumerate(saved_images, start=1):
        ext = os.path.splitext(filename)[1]
        new_filename = f"product_{product.id}_img{idx}{ext}"
        old_path = os.path.join(UPLOAD_DIR, filename)
        new_path = os.path.join(UPLOAD_DIR, new_filename)
        os.rename(old_path, new_path)
        final_images.append(new_filename)

    # Update product with final image names
    update_data = {
        "image": final_images[0],
        "images": final_images
    }
    return crud.update_product(db, product.id, update_data)


@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
        product_id: str,
        name: str = Form(None),
        description: str = Form(None),
        price: float = Form(None),
        rental_price: float = Form(None),
        type: str = Form(None),
        brand: str = Form(None),
        processor: str = Form(None),
        ram: str = Form(None),  # Changed from memory to ram
        storage: str = Form(None),
        display: str = Form(None),
        graphics: str = Form(None),
        availability: bool = Form(None),  # Changed from available to availability
        featured: bool = Form(None),
        images: List[UploadFile] = File(None),
        existing_images: List[str] = Form(None),  # For keeping existing images
        db: Session = Depends(get_db),
        user: dict = Depends(verify_admin_token)
):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Prepare update data
    update_data = {}
    if name is not None:
        update_data["name"] = name
    if description is not None:
        update_data["description"] = description
    if price is not None:
        update_data["price"] = price
    if rental_price is not None:
        update_data["rental_price"] = rental_price
    if type is not None:
        update_data["type"] = type
    if brand is not None:
        update_data["brand"] = brand
    if availability is not None:
        update_data["available"] = availability  # Map to available in DB
    if featured is not None:
        update_data["featured"] = featured

    # Handle specs
    specs = product.specs.copy() if product.specs else {}
    if processor is not None:
        specs["processor"] = processor
    if ram is not None:
        specs["memory"] = ram  # Map ram to memory in DB
    if storage is not None:
        specs["storage"] = storage
    if display is not None:
        specs["display"] = display
    if graphics is not None:
        specs["graphics"] = graphics
    update_data["specs"] = specs

    # Handle images
    if images or existing_images is not None:
        final_images = []

        # Keep existing images that weren't removed
        if existing_images is not None:
            if isinstance(existing_images, str):
                existing_images = [existing_images]  # Handle single image case
            final_images.extend(existing_images)

        # Add new images
        if images:
            for img in images:
                ext = os.path.splitext(img.filename)[1]
                filename = f"product_{product.id}_img{len(final_images) + 1}{ext}"
                filepath = os.path.join(UPLOAD_DIR, filename)

                async with aiofiles.open(filepath, "wb") as f:
                    content = await img.read()
                    await f.write(content)

                final_images.append(filename)

        # Validate at least one image
        if not final_images:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="At least one image is required"
            )

        update_data["image"] = final_images[0]
        update_data["images"] = final_images

    return crud.update_product(db, product_id, update_data)


@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(
        product_id: str,
        db: Session = Depends(get_db),
        user: dict = Depends(verify_admin_token)
):
    # Delete related cart entries
    cart_items = db.query(Cart).filter(Cart.product_id == product_id).all()
    for item in cart_items:
        db.delete(item)
    db.commit()

    # Delete the product
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Delete associated images
    for img in product.images:
        try:
            os.remove(os.path.join(UPLOAD_DIR, img))
        except OSError:
            pass

    return product