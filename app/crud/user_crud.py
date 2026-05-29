from sqlalchemy.orm import Session
from typing import List

# Import necessary components from your application structure
from .. import models
from ..schemas import user_schemas
from ..auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    """
    Fetches a single user from the database by their email address.
    """
    return db.query(models.user_model.User).filter(models.user_model.User.email == email).first()

def create_user(db: Session, user: user_schemas.UserCreate):
    """
    Creates a new user in the database.
    Hashes the password before storing it.
    """
    # Hash the plain text password from the request using our utility function
    hashed_password = get_password_hash(user.password)
    
    # Create a new SQLAlchemy User model instance
    db_user = models.user_model.User(
        email=user.email, 
        full_name=user.full_name, 
        password_hash=hashed_password
    )
    
    # Add the new user to the session, commit to the database, and refresh to get the new ID
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_skills(db: Session, user_id: int, skill_ids: List[int]):
    """
    Updates the skills for a specific user.
    It replaces the user's current list of skills with the new one.
    """
    # Find the user by their ID
    db_user = db.query(models.user_model.User).filter(models.user_model.User.id == user_id).first()
    if not db_user:
        return None # Return None if user not found

    # Find all the Skill objects corresponding to the provided IDs
    skills = db.query(models.skill_model.Skill).filter(models.skill_model.Skill.id.in_(skill_ids)).all()
    
    # Directly assign the new list of skills to the user's relationship.
    # SQLAlchemy is smart enough to handle the addition and removal of links
    # in the user_skills association table.
    db_user.skills = skills
    
    # Commit the changes to the database and refresh the user object
    db.commit()
    db.refresh(db_user)
    return db_user

