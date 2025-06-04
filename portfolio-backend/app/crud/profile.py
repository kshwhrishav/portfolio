from typing import Optional
from sqlalchemy.orm import Session
from app.models.profile import Profile
from app.schemas.profile import ProfileCreate, ProfileUpdate


def get_profile_by_user(db: Session, user_id: int) -> Optional[Profile]:
    """Retrieve a profile using the user's ID."""
    return db.query(Profile).filter(Profile.user_id == user_id).first()


def create_user_profile(
    db: Session, profile: ProfileCreate, user_id: int
) -> Profile:
    """Create a profile for the user."""
    db_profile = Profile(**profile.dict(), user_id=user_id)
    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def update_profile(
    db: Session, user_id: int, profile_update: ProfileUpdate
) -> Optional[Profile]:
    """Update a user profile."""
    db_profile = get_profile_by_user(db, user_id=user_id)
    if not db_profile:
        return None

    update_data = profile_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_profile, field, value)

    db.add(db_profile)
    db.commit()
    db.refresh(db_profile)
    return db_profile


def delete_profile(db: Session, user_id: int) -> Optional[Profile]:
    """Delete a user's profile."""
    db_profile = get_profile_by_user(db, user_id=user_id)
    if not db_profile:
        return None

    db.delete(db_profile)
    db.commit()
    return db_profile
