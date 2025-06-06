from fastapi import APIRouter
from app.crud.experience import (
    create_user_experience,
    update_user_experience,
    delete_user_experience,
    get_user_experience
)
from app.schemas.experience import ExperienceCreate, ExperienceUpdate

router = APIRouter()

@router.post("/experience")
def create_experience(experience: ExperienceCreate, user_id: int):
    return create_user_experience(experience, user_id)

@router.put("/experience/{experience_id}")
def update_experience(experience_id: int, experience: ExperienceUpdate, user_id: int):
    return update_user_experience(experience_id, experience, user_id)

@router.delete("/experience/{experience_id}")
def delete_experience(experience_id: int, user_id: int):
    return delete_user_experience(experience_id, user_id)

@router.get("/experience")
def get_experience(user_id: int):
    return get_user_experience(user_id) 