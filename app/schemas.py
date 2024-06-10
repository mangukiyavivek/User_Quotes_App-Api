# app/schemas.py
from typing import Optional
from pydantic import BaseModel

class UserBase(BaseModel):
    name: str
    email: str
    quotes: Optional[str] = None

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
