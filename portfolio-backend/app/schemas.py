from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    full_name: str
    password: str

class UserRead(UserBase):
    id: int
    full_name: str

class UserUpdate(UserBase):
    full_name: Optional[str] = None
    password: Optional[str] = None
    updated_at: Optional[datetime] = None

class UserResponse(UserBase):
    id: int
    full_name: str  
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # replaces orm_mode=True in Pydantic v2
    }
