from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.scheme.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud
import os
from datetime import datetime
from fastapi.responses import JSONResponse
from app.auth.jwt_handler import verify_admin_token  # adjust import as needed

import uuid
import aiofiles
from app.models.cart import Cart  # or wherever your Cart model is

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "static/uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/", response_model=list[ProductOut])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: str, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductOut)
async def create_product(
    name: str = Form(...),
    description: str = Form(...),
    price: float = Form(...),
    rental_price: float = Form(...),
    type: str = Form(...),
    brand: str = Form(...),
    processor: str = Form(...),
    memory: str = Form(...),
    storage: str = Form(...),
    display: str = Form(...),
    graphics: str = Form(...),
    available: bool = Form(...),
    featured: bool = Form(...),
    images: list[UploadFile] = File(...),  # Accept 4 images
    db: Session = Depends(get_db),
user: dict = Depends(verify_admin_token)
):
    # Step 1: Save images temporarily
    temp_file_paths = []
    for img in images:
        ext = os.path.splitext(img.filename)[1]
        temp_filename = f"{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        async with aiofiles.open(temp_path, "wb") as f:
            content = await img.read()
            await f.write(content)
        temp_file_paths.append((temp_filename, ext))

    # Step 2: Create product with first image temporarily
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "rental_price": rental_price,
        "type": type,
        "brand": brand,
        "image": temp_file_paths[0][0],  # Temporarily set first image
        "available": available,
        "featured": featured,
        "specs": {
            "processor": processor,
            "memory": memory,
            "storage": storage,
            "display": display,
            "graphics": graphics
        }
    }

    product_schema = ProductCreate(**product_data)
    product = crud.create_product(db, product_schema)

    # Step 3: Rename image files with product ID
    renamed_images = []
    for idx, (temp_name, ext) in enumerate(temp_file_paths, start=1):
        new_filename = f"product_image_{idx}_{product.id}{ext}"
        os.rename(
            os.path.join(UPLOAD_DIR, temp_name),
            os.path.join(UPLOAD_DIR, new_filename)
        )
        renamed_images.append(new_filename)

    # Step 4: Update product with renamed first image (you can update all if needed)
    updated = ProductUpdate(image=renamed_images[0])
    updated_product = crud.update_product(db, product.id, updated)

    # Optional: If storing all images, you could add them in a separate table or as a JSON field
    # Example: crud.save_product_images(db, product.id, renamed_images)

    return updated_product

@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str,
    updated: ProductUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)  # 🔒 Lock system here
):
    updated_data = updated.dict(exclude_unset=True)
    product = crud.update_product(db, product_id, updated_data)

    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product


@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    # 🛑 Step 1: Check and delete related cart entries
    cart_items = db.query(Cart).filter(Cart.product_id == product_id).all()
    for item in cart_items:
        db.delete(item)
    db.commit()

    # ✅ Step 2: Now delete the product safely
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    return product
