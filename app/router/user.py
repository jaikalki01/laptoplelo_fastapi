from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from passlib.hash import bcrypt

from app.database import SessionLocal
from app.models import User as UserModel
from app.scheme.user import UserCreate, User, Token, ChangePasswordRequest
from app.auth.jwt_handler import create_access_token, verify_token, verify_admin_token
from app.crud import user as user_crud

router = APIRouter(prefix="/users", tags=["Users"])

# --- Dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Signup Route (Open for all) ---
@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = bcrypt.hash(user.password)
    db_user = UserModel(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role,
        kyc_verified=user.kyc_verified,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Login Route (Open for all) ---
@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.email == form_data.username).first()
    if not user or not bcrypt.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(data={"user_id": user.id, "sub": user.email, "role": user.role})
    return {"access_token": token, "token_type": "bearer"}

# --- Authenticated User (User Profile) ---
@router.get("/auth", response_model=User)
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# --- Change Password (Any logged-in user) ---
@router.post("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    token_data: dict = Depends(verify_token)
):
    email = token_data.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Unauthorized")

    user = db.query(UserModel).filter(UserModel.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.verify(payload.current_password, user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")

    if bcrypt.verify(payload.new_password, user.password):
        raise HTTPException(status_code=400, detail="New password cannot be the same as current password")

    user.password = bcrypt.hash(payload.new_password)
    db.commit()

    return {"message": "Password changed successfully"}

# --- List All Users (Admin only) ---
@router.get("/", response_model=list[User])
def list_users(
    db: Session = Depends(get_db),
    token: dict = Depends(verify_admin_token),  # 🔒 Only admin can access
    search_term: str = "",
    role: str = "all",
    kyc_status: str = "all"
):
    return user_crud.get_users(db, search_term, role, kyc_status)

# --- Get User By ID (Admin only) ---
@router.get("/{user_id}", response_model=User)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_admin_token)  # 🔒 Only admin can access
):
    return user_crud.get_user_by_id(db, user_id)

# --- Example: Delete User (Admin only) ---
@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    token: dict = Depends(verify_admin_token)  # 🔒 Only admin can delete
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
