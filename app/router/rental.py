from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.scheme.rental import RentalCreate, RentalUpdate, RentalOut
from app.crud import rental as crud
from app.database import get_db
from typing import List

router = APIRouter(prefix="/rentals", tags=["Rentals"])

@router.get("/", response_model=List[RentalOut])
def read_rentals(db: Session = Depends(get_db)):
    return crud.get_all_rentals(db)

@router.post("/", response_model=RentalOut)
def create_rental(rental: RentalCreate, db: Session = Depends(get_db)):
    return crud.create_rental(db, rental)

@router.patch("/{rental_id}", response_model=RentalOut)
def update_rental_status(rental_id: str, rental_update: RentalUpdate, db: Session = Depends(get_db)):
    updated = crud.update_rental_status(db, rental_id, rental_update)
    if not updated:
        raise HTTPException(status_code=404, detail="Rental not found")
    return updated

@router.delete("/{rental_id}")
def delete_rental(rental_id: str, db: Session = Depends(get_db)):
    deleted = crud.delete_rental(db, rental_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Rental not found")
    return {"detail": "Rental deleted"}
