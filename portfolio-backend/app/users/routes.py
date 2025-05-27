from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models
from app.database import get_db
from app.auth.utils import get_current_user

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing = crud.get_user_by_email(db, email=user.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)

@router.get("/me", response_model=schemas.UserResponse)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/{id}", response_model=schemas.UserResponse)
def read_user_by_id(id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{id}", response_model=schemas.UserResponse)
def update_user_by_id(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = crud.get_user_by_id(db, id)
    if current_user.email != existing.email:
        raise HTTPException(status_code=403, detail="You are not authorized to update this user")
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.update_user(db, id, user)

@router.delete("/{id}")
def delete_user_by_id(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    existing = crud.get_user_by_id(db, id)
    if current_user.email != existing.email:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this user")
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    crud.delete_user(db, id)
    return {"message": "User deleted successfully"}

