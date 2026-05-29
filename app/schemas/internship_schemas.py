from pydantic import BaseModel
from typing import List, Optional
from .skill_schemas import Skill
from .company_schemas import Company

# Base schema for an internship's core data
class InternshipBase(BaseModel):
    title: str
    description: str
    location: Optional[str] = None
    company_id: int

# Schema used when creating a new internship
# It includes a list of skill IDs to be linked.
class InternshipCreate(InternshipBase):
    skill_ids: List[int] = []

# Schema used when returning an internship from the API.
# This will include the full company and skill objects.
class Internship(InternshipBase):
    id: int
    company: Company
    skills: List[Skill] = []

    class Config:
        from_attributes = True
