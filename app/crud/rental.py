
from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.scheme.rental import RentalCreate, RentalUpdate
import uuid

def create_rental(db: Session, rental: RentalCreate):
    db_rental = Rental(**rental.dict())  # ✅ No ID manually set
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental



def get_all_rentals(db: Session):
    return db.query(Rental).all()

def update_rental_status(db: Session, rental_id: str, update_data: RentalUpdate):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if rental:
        rental.status = update_data.status
        db.commit()
        db.refresh(rental)
    return rental

def delete_rental(db: Session, rental_id: str):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if rental:
        db.delete(rental)
        db.commit()
    return rental
