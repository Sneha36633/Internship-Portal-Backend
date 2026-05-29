from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship # <-- 1. Import relationship
from ..config.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    internship_id = Column(Integer, ForeignKey("internships.id"), nullable=False)
    match_score = Column(Float, nullable=False)
    
    # 2. This line creates the 'internship' attribute, allowing us to easily
    # access the full Internship object from a Recommendation object.
    internship = relationship("Internship")

