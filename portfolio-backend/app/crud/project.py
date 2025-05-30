from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate

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
