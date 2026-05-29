from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas, auth
from ..config.database import get_db

router = APIRouter()

@router.get("/recommendations/", response_model=List[schemas.recommendation_schemas.Recommendation])
def get_user_recommendations(
    current_user: schemas.user_schemas.User = Depends(auth.get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Get a list of AI-powered internship recommendations for the currently logged-in user.
    """
    recommendations = crud.recommendation_crud.get_recommendations_for_user(db, user_id=current_user.id)
    
    # We need to reshape the data to match the Pydantic schema
    response_data = []
    for rec in recommendations:
        response_data.append({
            "match_score": rec.match_score,
            "internship": rec.internship # Assuming you have a relationship set up in your model
        })

    return response_data
