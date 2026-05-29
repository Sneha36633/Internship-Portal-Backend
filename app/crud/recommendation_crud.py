from sqlalchemy.orm import Session
from .. import models

def get_recommendations_for_user(db: Session, user_id: int, limit: int = 10):
    """
    Fetches the top N recommendations for a given user, ordered by match_score.
    """
    recommendations = (
        db.query(models.recommendation_model.Recommendation)
        .filter(models.recommendation_model.Recommendation.user_id == user_id)
        .order_by(models.recommendation_model.Recommendation.match_score.desc())
        .limit(limit)
        .all()
    )
    return recommendations
