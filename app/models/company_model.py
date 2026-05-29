from sqlalchemy import Column, Integer, String, Text
from ..config.database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    website = Column(String, nullable=True)

