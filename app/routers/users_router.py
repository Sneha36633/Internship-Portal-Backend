from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

# Import necessary components from your application structure
from ..schemas import user_schemas
from ..crud import user_crud
from ..auth import get_current_user
from ..config.database import get_db

# Create a new router instance
router = APIRouter()

@router.get("/users/me", response_model=user_schemas.User)
def read_users_me(current_user: user_schemas.User = Depends(get_current_user)):
    """
    Fetch the profile of the currently logged-in user.
    The `get_current_user` dependency handles all the token verification.
    If the token is invalid or missing, it will automatically send a 401 Unauthorized error.
    """
    # The dependency already fetches the user object, so we can just return it.
    return current_user

@router.put("/users/me/skills", response_model=user_schemas.User)
def update_my_skills(
    skills_update: user_schemas.UserSkillsUpdate,
    current_user: user_schemas.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update the skills for the currently logged-in user.
    This endpoint expects a JSON body with a list of skill IDs.
    """
    # Call the CRUD function to update the skills in the database
    updated_user = user_crud.update_user_skills(
        db=db, user_id=current_user.id, skill_ids=skills_update.skill_ids
    )
    return updated_user

