from sqlalchemy.orm import Session
from app.models.address import Address
from app.scheme.address import AddressCreate

def add_address(db: Session, user_id: int, address_data: AddressCreate):
    if address_data.is_default:
        # Unset other default addresses for this user
        db.query(Address).filter(Address.user_id == user_id, Address.is_default == True).update(
            {"is_default": False}
        )
    new_address = Address(
        street=address_data.street,
        city=address_data.city,
        state=address_data.state,
        pincode=address_data.pincode,
        is_default=address_data.is_default,
        user_id=user_id
    )
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def update_address(db: Session, address_id: int, address_data: AddressCreate):
    # Fetch the address to update
    address = db.query(Address).filter(Address.id == address_id).first()

    if not address:
        return None  # Return None if the address does not exist

    # Update the address fields
    address.street = address_data.street
    address.city = address_data.city
    address.state = address_data.state
    address.pincode = address_data.pincode
    address.is_default = address_data.is_default

    db.commit()
    db.refresh(address)

    return address

def get_addresses_by_user(db: Session, user_id: int):
    return db.query(Address).filter(Address.user_id == user_id).all()

def get_address_by_id(db: Session, address_id: int):
    return db.query(Address).filter(Address.id == address_id).first()
