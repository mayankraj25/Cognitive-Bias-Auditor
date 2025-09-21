from pydantic import BaseModel
from typing import Optional
import datetime

# --- Reflection & Analysis Schemas ---
class Analysis(BaseModel):
    content: str
    timestamp: datetime.datetime

    class Config:
        from_attributes = True

class ReflectionBase(BaseModel):
    content: str

class ReflectionCreate(ReflectionBase):
    pass

class Reflection(ReflectionBase):
    id: int
    timestamp: datetime.datetime
    owner_id: int
    analysis: Optional[Analysis] = None

    class Config:
        from_attributes = True

# --- User Schemas ---
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    reflections: list[Reflection] = []

    class Config:
        from_attributes = True

# --- Token Schema ---
class Token(BaseModel):
    access_token: str
    token_type: str