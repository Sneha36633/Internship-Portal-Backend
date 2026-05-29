from sqlalchemy.orm import Session
from .. import models, schemas

def get_skill_by_name(db: Session, name: str):
    return db.query(models.skill_model.Skill).filter(models.skill_model.Skill.name == name).first()

def create_skill(db: Session, skill: schemas.skill_schemas.SkillCreate):
    db_skill = models.skill_model.Skill(name=skill.name)
    db.add(db_skill)
    db.commit()
    db.refresh(db_skill)
    return db_skill

def get_skills(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.skill_model.Skill).offset(skip).limit(limit).all()
