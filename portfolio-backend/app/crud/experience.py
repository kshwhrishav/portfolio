from sqlalchemy.orm import Session
from app.models.experience import Experience
from app.schemas.experience import ExperienceCreate, ExperienceUpdate


def create_user_experience(db: Session, experience: ExperienceCreate, user_id: int):
    db_experience = Experience(
        title=experience.title,
        company=experience.company,
        location=experience.location,
        type=experience.type,
        start_date=experience.start_date,
        end_date=experience.end_date,
        is_current=experience.is_current,
        description=experience.description,
        user_id=user_id
    )
    db.add(db_experience)
    db.commit()
    db.refresh(db_experience)
    return db_experience


def update_user_experience(db: Session, experience_id: int, experience: ExperienceUpdate, user_id: int):
    db_experience = db.query(Experience).filter(Experience.id == experience_id, Experience.user_id == user_id).first()
    if not db_experience:
        return None

    if experience.title is not None:
        db_experience.title = experience.title
    if experience.company is not None:
        db_experience.company = experience.company
    if experience.location is not None:
        db_experience.location = experience.location
    if experience.type is not None:
        db_experience.type = experience.type
    if experience.start_date is not None:
        db_experience.start_date = experience.start_date
    if experience.end_date is not None:
        db_experience.end_date = experience.end_date
    if experience.is_current is not None:
        db_experience.is_current = experience.is_current
    if experience.description is not None:
        db_experience.description = experience.description

    db.commit()
    db.refresh(db_experience)
    return db_experience


def delete_user_experience(db: Session, experience_id: int, user_id: int):
    db_experience = db.query(Experience).filter(Experience.id == experience_id, Experience.user_id == user_id).first()
    if not db_experience:
        return False
    db.delete(db_experience)
    db.commit()
    return True


def get_user_experience(db: Session, user_id: int):
    return db.query(Experience).filter(Experience.user_id == user_id).all()
