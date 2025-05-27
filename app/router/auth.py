from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.scheme.auth import ForgotPasswordRequest, ResetPasswordRequest
from app.auth.jwt_handler import create_reset_token, verify_reset_token
from app.auth.email import send_reset_email
from app.crud import user as user_crud
from passlib.context import CryptContext
from app.database import SessionLocal


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest, db: Session = Depends(get_db)):
    db_user = user_crud.get_user_by_email(db, request.email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    token = create_reset_token(request.email)
    send_reset_email(request.email, token)
    return {"message": "Reset link sent to your email"}


@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest, db: Session = Depends(get_db)):
    email = verify_reset_token(request.token)
    if not email:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    db_user = user_crud.get_user_by_email(db, email)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = pwd_context.hash(request.new_password)
    user_crud.update_user_password(db, db_user, hashed_password)
    return {"message": "Password has been reset"}
