from typing import Optional
from datetime import datetime
from pydantic import BaseModel, HttpUrl


class ProfileBase(BaseModel):
    headline: str
    summary: str
    location: Optional[str] = None
    website: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(BaseModel):
    headline: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[str] = None
    website: Optional[HttpUrl] = None
    linkedin: Optional[HttpUrl] = None
    github: Optional[HttpUrl] = None


class ProfileOut(ProfileBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
