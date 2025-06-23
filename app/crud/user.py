from sqlalchemy.orm import Session
from app.models.user import User  # Ensure you import the correct User model
from app.models.user import User
from passlib.hash import bcrypt
from app.models.user import User
from app.scheme.user import UserCreate


def create_user(db: Session, user_data: UserCreate):
    hashed_password = bcrypt.hash(user_data.password)
    db_user = User(
        name=user_data.name,
        email=user_data.email,
        password=hashed_password,
        role=user_data.role,
        kyc_verified=user_data.kyc_verified,
    )

    # Add the user to the session and commit
    db.add(db_user)
    db.commit()
    db.refresh(db_user)  # Refresh the user to get the generated ID

    return db_user


def get_users(db: Session, search_term: str = None, role: str = None, kyc_status: str = None):
    query = db.query(User)

    if search_term:
        query = query.filter(
            User.name.ilike(f"%{search_term}%") |
            User.email.ilike(f"%{search_term}%")
        )

    if role and role != "all":
        query = query.filter(User.role == role)

    if kyc_status:
        if kyc_status == "verified":
            query = query.filter(User.kyc_verified == True)
        elif kyc_status == "unverified":
            query = query.filter(User.kyc_verified == False)

    return query.all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def update_user_password(db: Session, user: User, hashed_password: str):
    user.password = hashed_password
    db.commit()
    db.refresh(user)
