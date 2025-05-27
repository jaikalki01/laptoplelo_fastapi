from fastapi import APIRouter, HTTPException,Depends
from app.scheme.contact import ContactForm, ContactOut
from app.auth.mailer import send_contact_email
from sqlalchemy.orm import Session
from app.crud.contact import create_contact
from app.database import SessionLocal
from app.crud.contact import create_contact, get_all_contacts
from app.auth.jwt_handler import verify_admin_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/contact")
async def submit_contact_form(form: ContactForm, db: Session = Depends(get_db)):
    # Save to database
    try:
        create_contact(db, form)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to save contact form.")

    # Send email
    success = send_contact_email(form.name, form.email, form.phone, form.message)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to send email.")

    return {"message": "Contact form submitted successfully."}

@router.get("/contact", response_model=list[ContactOut])
def get_all_contact_messages(
    db: Session = Depends(get_db),
    _: dict = Depends(verify_admin_token)  # ✅ Apply admin token verification
):
    try:
        return get_all_contacts(db)
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to fetch contact list.")
