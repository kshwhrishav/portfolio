from typing import List, Optional

from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.models.user import User
from app.models.project import Project
from app.schemas.user import UserCreate, UserUpdate
from app.schemas.project import ProjectCreate, ProjectUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate) -> User:
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

def delete_user(db: Session, user_id: int) -> None:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    db.delete(user)
    db.commit()


def update_user(db: Session, user_id: int, user_data: UserUpdate) -> User:
    existing = db.query(User).filter(User.id == user_id).first()
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

# Project CRUD operations
def get_project(db: Session, project_id: int) -> Optional[Project]:
    """Get a project by ID."""
    return db.query(Project).filter(Project.id == project_id).first()

def get_projects_by_user(
    db: Session, 
    user_id: int, 
    skip: int = 0, 
    limit: int = 100
) -> List[Project]:
    """Get all projects for a specific user with pagination."""
    return (
        db.query(Project)
        .filter(Project.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def create_user_project(
    db: Session, 
    project: ProjectCreate, 
    user_id: int
) -> Project:
    """Create a new project for a specific user."""
    db_project = Project(**project.dict(), user_id=user_id)
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def update_project(
    db: Session, 
    project_id: int, 
    project: ProjectUpdate
) -> Optional[Project]:
    """Update a project's information."""
    db_project = get_project(db, project_id=project_id)
    if not db_project:
        return None
    
    update_data = project.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project

def delete_project(db: Session, project_id: int) -> Optional[Project]:
    """Delete a project by ID."""
    db_project = get_project(db, project_id=project_id)
    if not db_project:
        return None
    
    db.delete(db_project)
    db.commit()
    return db_project
