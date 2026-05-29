from sqlalchemy.orm import Session
from typing import List

from .. import models
from ..schemas import user_schemas
from ..auth import get_password_hash


# ---------------- GET USER BY EMAIL ----------------
def get_user_by_email(db: Session, email: str):
    return (
        db.query(models.user_model.User)
        .filter(models.user_model.User.email == email)
        .first()
    )


# ---------------- CREATE USER ----------------
def create_user(db: Session, user: user_schemas.UserCreate):

    hashed_password = get_password_hash(user.password)

    db_user = models.user_model.User(
        email=user.email,
        full_name=user.full_name,
        password_hash=hashed_password
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


# ---------------- UPDATE USER SKILLS ----------------
def update_user_skills(db: Session, user_id: int, skill_ids: List[int]):

    db_user = (
        db.query(models.user_model.User)
        .filter(models.user_model.User.id == user_id)
        .first()
    )

    if not db_user:
        return None

    # ✅ SAFE CHECK (IMPORTANT FIX)
    if not skill_ids:
        db_user.skills = []
        db.commit()
        db.refresh(db_user)
        return db_user

    # FIX: avoid crash on empty / invalid input
    skills = (
        db.query(models.skill_model.Skill)
        .filter(models.skill_model.Skill.id.in_(skill_ids))
        .all()
    )

    db_user.skills = skills

    db.commit()
    db.refresh(db_user)

    return db_user