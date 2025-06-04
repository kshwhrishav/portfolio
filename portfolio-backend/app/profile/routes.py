from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.auth.utils import get_current_user

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=schemas.ProfileOut)
def read_profile(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Get the current user's profile."""
    profile = crud.get_profile_by_user(db, user_id=current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/", response_model=schemas.ProfileOut, status_code=status.HTTP_201_CREATED)
def create_profile(
    profile_in: schemas.ProfileCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Create a profile for the current user."""
    existing = crud.get_profile_by_user(db, user_id=current_user.id)
    if existing:
        raise HTTPException(status_code=400, detail="Profile already exists")

    return crud.create_user_profile(db=db, profile=profile_in, user_id=current_user.id)


@router.put("/", response_model=schemas.ProfileOut)
def update_profile(
    profile_in: schemas.ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """Update the current user's profile."""
    updated = crud.update_profile(db=db, user_id=current_user.id, profile_update=profile_in)
    if not updated:
        raise HTTPException(status_code=404, detail="Profile not found")
    return updated
