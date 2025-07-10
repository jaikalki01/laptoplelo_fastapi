
from ..auth.jwt_handler import verify_token, verify_admin_token

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session
from typing import List, Optional
import os, uuid, aiofiles
from ..database import get_db
from ..models import Product
from ..scheme.product import ProductOut
from app.models import Product as ProductModel, Cart as CartModel

class Settings:
    BASE_URL: str = os.getenv("BASE_URL", "")
    STATIC_DIR: str = os.getenv("STATIC_DIR", "static")
    UPLOAD_DIR: str = os.path.join(STATIC_DIR, "uploaded_images")

    class Config:
        env_file = ".env"


settings = Settings()
router = APIRouter(prefix="/products", tags=["Products"])
UPLOAD_DIR = os.path.join(settings.STATIC_DIR, "uploaded_images")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image_urls(product: Product) -> Product:
    if product.image:
        product.image = f"/static/uploaded_images/{os.path.basename(product.image)}"

    if product.images:
        product.images = [
            f"/static/uploaded_images/{os.path.basename(img)}"
            for img in product.images
        ]
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
        memory: str = Form(...),
        storage: str = Form(...),
        display: str = Form(...),
        graphics: str = Form(...),
        available: bool = Form(True),
        featured: bool = Form(False),
        images: List[UploadFile] = File(...),
        db: Session = Depends(get_db)
):
    # Validate at least one image
    if not images:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one image is required"
        )

    # Process specs
    specs = {
        "processor": processor,
        "memory": memory,
        "storage": storage,
        "display": display,
        "graphics": graphics,
    }

    # Save images
    saved_images = []
    for img in images[:4]:  # Limit to 4 images
        ext = os.path.splitext(img.filename)[1]
        filename = f"{uuid.uuid4().hex}{ext}"
        filepath = os.path.join(UPLOAD_DIR, filename)

        async with aiofiles.open(filepath, "wb") as buffer:
            await buffer.write(await img.read())

        saved_images.append(filename)

    # Create product
    product = Product(
        name=name,
        description=description,
        price=price,
        rental_price=rental_price,
        type=type,
        brand=brand,
        specs=specs,
        images=saved_images,
        image=saved_images[0],
        available=available,
        featured=featured
    )

    db.add(product)
    db.commit()
    db.refresh(product)
    return save_image_urls(product)


@router.get("/", response_model=List[ProductOut])
def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return [save_image_urls(p) for p in products]


@router.get("/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Not found")
    return save_image_urls(product)




@router.put("/{product_id}", response_model=ProductOut)
async def update_product(
        product_id: int,
        name: Optional[str] = Form(None),
        description: Optional[str] = Form(None),
        price: Optional[float] = Form(None),
        rental_price: Optional[float] = Form(None),
        type: Optional[str] = Form(None),
        brand: Optional[str] = Form(None),
        processor: Optional[str] = Form(None),
        memory: Optional[str] = Form(None),
        storage: Optional[str] = Form(None),
        display: Optional[str] = Form(None),
        graphics: Optional[str] = Form(None),
        available: Optional[bool] = Form(None),
        featured: Optional[bool] = Form(None),
        existing_images: Optional[str] = Form(None),  # comma-separated
        new_images: Optional[List[UploadFile]] = File(None),
        db: Session = Depends(get_db)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    # Update basic fields
    update_data = {
        "name": name,
        "description": description,
        "price": price,
        "rental_price": rental_price,
        "type": type,
        "brand": brand,
        "available": available,
        "featured": featured
    }

    for field, value in update_data.items():
        if value is not None:
            setattr(product, field, value)

    # Update specs
    if any([processor, memory, storage, display, graphics]):
        specs = product.specs or {}
        if processor: specs["processor"] = processor
        if memory: specs["memory"] = memory
        if storage: specs["storage"] = storage
        if display: specs["display"] = display
        if graphics: specs["graphics"] = graphics
        product.specs = specs

    # Handle images
    keep_images = []
    if existing_images:
        keep_images = [
            os.path.basename(img.strip())
            for img in existing_images.split(",")
            if img.strip()
        ]

    # Add new images
    if new_images:
        for img in new_images[:4 - len(keep_images)]:  # Enforce 4 image limit
            ext = os.path.splitext(img.filename)[1]
            filename = f"{uuid.uuid4().hex}{ext}"
            filepath = os.path.join(UPLOAD_DIR, filename)

            async with aiofiles.open(filepath, "wb") as buffer:
                await buffer.write(await img.read())

            keep_images.append(filename)

    # Delete removed images
    current_images = product.images or []
    for old_img in current_images:
        if old_img not in keep_images:
            try:
                os.remove(os.path.join(UPLOAD_DIR, old_img))
            except FileNotFoundError:
                pass

    # Update product images
    product.images = keep_images
    product.image = keep_images[0] if keep_images else None

    db.commit()
    db.refresh(product)
    return save_image_urls(product)


@router.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    # Step 1: Remove product from all carts
    db.query(CartModel).filter(CartModel.product_id == product_id).delete()

    # Step 2: Find and delete the product
    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return {"message": "Product deleted successfully"}
