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
    first_name: str
    last_name: str
    role: str
    password: str

class UserRead(UserBase):
    id: int
    first_name: str
    last_name: str
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserUpdate(UserBase):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[str] = None
    password: Optional[str] = None
    updated_at: Optional[datetime] = None

class UserResponse(UserBase):
    id: int
    first_name: str
    last_name: str
    role: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = {
        "from_attributes": True  # replaces orm_mode=True in Pydantic v2
    }
