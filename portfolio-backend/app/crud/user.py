from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get a user by email."""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    """Get a user by ID."""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user with hashed password."""
    hashed_pw = pwd_context.hash(user.password)
    db_user = User(
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        role=user.role,
        hashed_password=hashed_pw
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
    """Update a user's information."""
    existing = get_user_by_id(db, user_id=user_id)
    if not existing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update only the fields that are provided in the update data
    update_data = user_data.dict(exclude_unset=True)
    if 'password' in update_data and update_data['password'] is not None:
        hashed_password = pwd_context.hash(update_data['password'])
        update_data['hashed_password'] = hashed_password
        del update_data['password']
    
    for field, value in update_data.items():
        setattr(existing, field, value)
    
    db.add(existing)
    db.commit()
    db.refresh(existing)
    return existing

def delete_user(db: Session, user_id: int) -> None:
    """Delete a user by ID."""
    user = get_user_by_id(db, user_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()
