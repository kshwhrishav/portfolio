from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse
from app.models.project import Project
from app.database import get_db
from app.auth.utils import get_current_user
from app.crud.project import (
    get_project,
    get_projects_by_user,
    create_user_project,
    update_project,
    delete_project
)

from app.models.user import User

router = APIRouter(prefix="/projects", tags=["Projects"])

@router.get("/projects/{user_id}", response_model=list[ProjectResponse])
def read_projects_by_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return get_projects_by_user(db, user_id=user_id)

@router.post("/projects", response_model=ProjectResponse)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_user_project(db, project=project, user_id=current_user.id)    

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project_by_id(
    project_id: int,
    project: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return update_project(db, project_id=project_id, project=project)

@router.delete("/projects/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project_by_id(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return delete_project(db, project_id=project_id)