from http.client import HTTPException

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload
from app.database import get_db
from app.models import Rental, User, Product
from app.scheme.rental import RentalCreate, RentalOut

from typing import List

router = APIRouter(prefix="/rentals", tags=["Rentals"])


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models import Rental

@router.get("/rentals", response_model=list[RentalOut])
def get_rentals(db: Session = Depends(get_db)):
    rentals = db.query(Rental).all()
    return rentals

@router.post("/", response_model=RentalOut)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    # Validate user and product
    user = db.query(User).filter(User.id == rental.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product = db.query(Product).filter(Product.id == rental.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Create rental
    new_rental = Rental(**rental.dict())
    db.add(new_rental)
    db.commit()
    db.refresh(new_rental)
    return new_rental