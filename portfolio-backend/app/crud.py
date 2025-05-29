from sqlalchemy.orm import Session
from app import models, schemas
from passlib.context import CryptContext
from fastapi import HTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_id(db: Session, id: int):
    return db.query(models.User).filter(models.User.id == id).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_pw = pwd_context.hash(user.password)
    db_user = models.User(email=user.email, first_name=user.first_name, last_name=user.last_name, role=user.role, hashed_password=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, id: int):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}

def update_user(db: Session, id: int, user: schemas.UserUpdate):
    existing = db.query(models.User).filter(models.User.id == id).first()
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    existing.first_name = user.first_name
    existing.last_name = user.last_name
    existing.hashed_password = pwd_context.hash(user.password)
    db.commit()
    db.refresh(existing)
    return existing
    
