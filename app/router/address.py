from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.address import add_address, get_addresses_by_user , update_address
from app.scheme.address import AddressCreate, Address
from app.models.user import  User as UserModel
from app.models.address import Address as AddressModel
from app.auth.jwt_handler import verify_user_token

router = APIRouter(prefix="/users", tags=["Addresses"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/{user_id}/addresses", response_model=Address)
def add_user_address(
    user_id: int,
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    token_user_id: int = Depends(verify_user_token)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user’s data")

    return add_address(db=db, user_id=user_id, address_data=address_data)


@router.get("/{user_id}/addresses", response_model=list[Address])
def get_user_addresses(
    user_id: int,
    db: Session = Depends(get_db),
    token_user_id: int = Depends(verify_user_token)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this user’s data")

    return get_addresses_by_user(db=db, user_id=user_id)


@router.put("/addresses/{address_id}", response_model=Address)
def edit_address(
    address_id: int,
    address_data: AddressCreate,
    db: Session = Depends(get_db),
    token_user_id: int = Depends(verify_user_token)
):
    # Optional: verify if address belongs to token_user_id
    updated_address = update_address(db, address_id, address_data)
    if not updated_address:
        raise HTTPException(status_code=404, detail="Address not found")
    return updated_address


@router.delete("/{user_id}/addresses/{address_id}", response_model=Address)
def delete_address(
    user_id: int,
    address_id: int,
    db: Session = Depends(get_db),
    token_user_id: int = Depends(verify_user_token)
):
    if user_id != token_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this address")

    address = db.query(AddressModel).filter(AddressModel.id == address_id, AddressModel.user_id == user_id).first()
    if not address:
        raise HTTPException(status_code=404, detail="Address not found")

    db.delete(address)
    db.commit()
    return address

