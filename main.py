from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.database import Base, engine
from app.router import (
    product, user, address, coupon, dashboard, auth, contact,
    cart, wishlist, pcbuild, transaction, analytics, rental
)
from app.router.product import settings

# Create DB tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/assets", StaticFiles(directory="static/dist/assets"), name="assets")

# Routers
app.include_router(product.router)
app.include_router(user.router)
app.include_router(address.router)
app.include_router(rental.router)
app.include_router(coupon.router)
app.include_router(dashboard.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(contact.router, tags=["Contact"])
app.include_router(cart.router)
app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])
app.include_router(pcbuild.router)
app.include_router(transaction.router)
app.include_router(analytics.router)

# Create upload directories if not exists
os.makedirs(settings.STATIC_DIR, exist_ok=True)
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Serve React root
@app.get("/")
async def serve_react():
    return FileResponse("static/dist/index.html")

# Serve all frontend routes (React SPA)
@app.get("/{full_path:path}")
async def serve_react_spa(full_path: str):
    file_path = os.path.join('static', 'dist', full_path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    return FileResponse("static/dist/index.html")


# Run using `python main.py`
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
