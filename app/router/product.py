from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.scheme.product import ProductCreate, ProductOut, ProductUpdate
from app.crud import product as crud
from app.auth.jwt_handler import verify_admin_token

import os
import uuid
import aiofiles

router = APIRouter(prefix="/products", tags=["Products"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

UPLOAD_DIR = "static/uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# ✅ Get All Products
@router.get("/", response_model=list[ProductOut])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_products(db, skip, limit)

# ✅ Get Single Product by ID
@router.get("/{product_id}", response_model=ProductOut)
def read_product(product_id: str, db: Session = Depends(get_db)):
    product = crud.get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ✅ Create Product with 4 Images
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
    images: list[UploadFile] = File(...),
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    if len(images) != 4:
        raise HTTPException(status_code=400, detail="Exactly 4 images required")

    temp_file_paths = []
    for img in images:
        ext = os.path.splitext(img.filename)[1]
        temp_filename = f"{uuid.uuid4().hex}{ext}"
        temp_path = os.path.join(UPLOAD_DIR, temp_filename)
        async with aiofiles.open(temp_path, "wb") as f:
            content = await img.read()
            await f.write(content)
        temp_file_paths.append((temp_filename, ext))

    # Create product with placeholder image
    product_data = {
        "name": name,
        "description": description,
        "price": price,
        "rental_price": rental_price,
        "type": type,
        "brand": brand,
        "image": temp_file_paths[0][0],
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

    # Rename and update image names with product ID
    renamed_images = []
    for idx, (temp_name, ext) in enumerate(temp_file_paths, start=1):
        new_filename = f"product_{product.id}_img_{idx}{ext}"
        os.rename(
            os.path.join(UPLOAD_DIR, temp_name),
            os.path.join(UPLOAD_DIR, new_filename)
        )
        renamed_images.append(new_filename)

    # Update product with final image name
    updated = ProductUpdate(image=renamed_images[0])
    updated_product = crud.update_product(db, product.id, updated)

    # Optional: Save all 4 image filenames (if needed)
    # crud.save_product_images(db, product.id, renamed_images)

    return updated_product

# ✅ Update Product
@router.put("/{product_id}", response_model=ProductOut)
def update_product(
    product_id: str,
    updated: ProductUpdate,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    updated_data = updated.dict(exclude_unset=True)
    product = crud.update_product(db, product_id, updated_data)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# ✅ Delete Product
@router.delete("/{product_id}", response_model=ProductOut)
def delete_product(
    product_id: str,
    db: Session = Depends(get_db),
    user: dict = Depends(verify_admin_token)
):
    product = crud.delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product
