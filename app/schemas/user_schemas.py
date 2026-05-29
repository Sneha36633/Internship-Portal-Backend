from pydantic import BaseModel
from typing import Optional, List

# 1. Import the Skill schema so we can use it
from .skill_schemas import Skill

# This defines the basic shape of a user+

class UserBase(BaseModel):
    email: str
    full_name: str
    phone_number: Optional[str] = None
    bio: Optional[str] = None

# This is used when creating a new user (it includes the password)
class UserCreate(UserBase):
    password: str

# This is the model that will be returned from the API (it doesn't include the password)
class User(UserBase):
    id: int
    # 2. Add the skills field. It will be a list of Skill objects.
    skills: List[Skill] = []

    class Config:
        from_attributes = True

# This defines the shape of a login request (just email and password)
class UserLogin(BaseModel):
    email: str
    password: str

# This defines the shape of the token response after login
class Token(BaseModel):
    access_token: str
    token_type: str

# NEW SCHEMA for updating user skills
class UserSkillsUpdate(BaseModel):
    skill_ids: List[int] = []

