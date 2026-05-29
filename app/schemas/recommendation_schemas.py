from pydantic import BaseModel
from .internship_schemas import Internship

class Recommendation(BaseModel):
    match_score: float
    internship: Internship

    class Config:
        from_attributes = True

