from pydantic import BaseModel
from typing import Optional, List

from .skill_schemas import Skill


# ---------------- USER BASE ----------------
class UserBase(BaseModel):
    email: str
    full_name: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None


# ---------------- CREATE USER ----------------
class UserCreate(UserBase):
    password: str


# ---------------- USER RESPONSE ----------------
class User(UserBase):
    id: int
    skills: List[Skill] = []

    class Config:
        from_attributes = True


# ---------------- LOGIN ----------------
class UserLogin(BaseModel):
    email: str
    password: str


# ---------------- TOKEN ----------------
class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------- UPDATE SKILLS ----------------
class UserSkillsUpdate(BaseModel):
    skill_ids: List[int] = []