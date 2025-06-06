from datetime import date
from typing import Optional
from app.schemas.base import BaseModel
from app.models.experience import ExperienceType


class ExperienceBase(BaseModel):
    title: str
    company: str
    location: Optional[str] = None
    type: ExperienceType
    start_date: date
    end_date: Optional[date] = None
    is_current: bool = False
    description: Optional[str] = None


class ExperienceCreate(ExperienceBase):
    pass


class ExperienceUpdate(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    location: Optional[str] = None
    type: Optional[ExperienceType] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    is_current: Optional[bool] = None
    description: Optional[str] = None


class ExperienceOut(ExperienceBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
