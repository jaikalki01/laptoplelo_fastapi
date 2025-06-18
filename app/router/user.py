from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.scheme.user import UserCreate, User
from app.crud import user as user_crud
from pydantic import BaseModel
from app.models import User as UserModel
from passlib.hash import bcrypt
from app.scheme.user import LoginForm
from app.scheme.user import Token
from fastapi.security import OAuth2PasswordRequestForm
from app.auth.jwt_handler import create_access_token
from app.auth.jwt_handler import verify_token,verify_admin_token
from app.auth.jwt_handler import verify_recaptcha
from app.scheme.user import ChangePasswordRequest


router = APIRouter(prefix="/users", tags=["Users"])

def get_db():
    db = SessionLocal()  # Assuming SessionLocal is defined somewhere
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    db_user = UserModel(
        name=user.name,
        email=user.email,
        role=user.role,
        kyc_verified=user.kyc_verified,
        password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user



@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # Fetch user from the database
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()

    if not user or not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
        )


    # Include the role in the token payload
    access_token = create_access_token(data={"user_id": user.id, "sub": user.email, "role": user.role})

    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth", response_model=User)
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=list[User])
def list_users(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_admin_token),  # Enforce admin-only access
    search_term: str = "",  # Add search term as query param
    role: str = "all",  # Add role filter
    kyc_status: str = "all"  # Add KYC status filter
):
    # Apply filters to query if necessary
    return user_crud.get_users(db, search_term, role, kyc_status)


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int, db: Session = Depends(get_db)):
    return user_crud.get_user_by_id(db, user_id)


@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    email = token_data.get("sub")
    user = db.query(UserModel).filter(UserModel.email == email).first()

    if not user or not bcrypt.verify(payload.current_password, user.password):
        raise HTTPException(
            status_code=400,
            detail="Current password is incorrect"
        )

    # Hash new password
    hashed_new_password = bcrypt.hash(payload.new_password)
    user.password = hashed_new_password
    db.commit()

    return {"message": "Password changed successfully"}
