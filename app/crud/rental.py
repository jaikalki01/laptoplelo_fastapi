from sqlalchemy.orm import Session
from app.models.rental import Rental
from app.scheme.rental import RentalCreate, RentalUpdateStatus
import uuid

def get_all_rentals(db: Session):
    return db.query(Rental).all()

def create_rental(db: Session, rental: RentalCreate):
    db_rental = Rental(
        id=str(uuid.uuid4()),
        **rental.dict()
    )
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

def delete_rental(db: Session, rental_id: str):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if rental:
        db.delete(rental)
        db.commit()
    return rental

def update_rental_status(db: Session, rental_id: str, status: str):
    rental = db.query(Rental).filter(Rental.id == rental_id).first()
    if rental:
        rental.status = status
        db.commit()
        db.refresh(rental)
    return rental
