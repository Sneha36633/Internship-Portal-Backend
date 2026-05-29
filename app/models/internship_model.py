from sqlalchemy import Column, Integer, String, Text, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..config.database import Base

# This is an association table for the many-to-many relationship
# between internships and skills.
internship_skills_table = Table('internship_skills', Base.metadata,
    Column('internship_id', Integer, ForeignKey('internships.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class Internship(Base):
    __tablename__ = "internships"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String, nullable=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)

    # Define the relationship to the Company model
    company = relationship("Company")
    
    # Define the many-to-many relationship to the Skill model
    skills = relationship("Skill", secondary=internship_skills_table)
