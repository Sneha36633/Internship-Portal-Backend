from sqlalchemy import Column, Integer, String, Text, Table, ForeignKey
from sqlalchemy.orm import relationship
from ..config.database import Base

# This is an "association table" for the many-to-many relationship
# between users and skills.
user_skills_table = Table('user_skills', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('skill_id', Integer, ForeignKey('skills.id'), primary_key=True)
)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    phone_number = Column(String, nullable=True)
    bio = Column(Text, nullable=True)

    # This line creates the 'skills' attribute on the User object.
    # It tells SQLAlchemy to link the User and Skill models using
    # the user_skills_table.
    skills = relationship("Skill", secondary=user_skills_table)
