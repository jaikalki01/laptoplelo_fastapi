from sys import prefix

from fastapi import FastAPI ,HTTPException
from app.database import Base, engine  # Assuming database.py is inside app/
from app.router import product, user, address, coupon, dashboard, auth, contact, cart, wishlist, \
    pcbuild, transaction, analytics  # Assuming product.py is inside app/router/
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles

from app.router import rental

# Create tables if not exist
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Include the router
app.include_router(product.router)
app.include_router(user.router)
app.include_router(address.router)
app.include_router(rental.router)
app.include_router(coupon.router)
app.include_router(dashboard.router)
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(contact.router ,tags=["Contact"])
app.include_router(cart.router)
app.include_router(wishlist.router, prefix="/wishlist", tags=["Wishlist"])
app.include_router(pcbuild.router)
app.include_router(transaction.router)
app.include_router(analytics.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
