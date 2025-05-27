from sqlalchemy.orm import Session
from app.models.contact import Contact
from app.scheme.contact import ContactForm


def create_contact(db: Session, form: ContactForm):
    db_contact = Contact(
        name=form.name,
        email=form.email,
        phone=form.phone,
        message=form.message,
    )
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact


def get_all_contacts(db: Session):
    return db.query(Contact).order_by(Contact.id.desc()).all()
