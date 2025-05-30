from datetime import datetime
from pydantic import BaseModel, HttpUrl
from typing import List, Optional

class ProjectBase(BaseModel):
    title: str
    description: Optional[str] = None
    tech_stack: Optional[List[str]] = None
    live_url: Optional[HttpUrl] = None
    github_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    title: Optional[str] = None
    description: Optional[str] = None

class ProjectInDBBase(ProjectBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ProjectResponse(ProjectInDBBase):
    pass
