from sqlalchemy.orm import Session
from .. import models, schemas

def create_internship(db: Session, internship: schemas.internship_schemas.InternshipCreate):
    # Create the main internship object without the skill_ids
    db_internship = models.internship_model.Internship(
        title=internship.title,
        description=internship.description,
        location=internship.location,
        company_id=internship.company_id
    )
    db.add(db_internship)
    db.commit()
    db.refresh(db_internship)

    # Now, link the skills to the internship
    if internship.skill_ids:
        skills = db.query(models.skill_model.Skill).filter(models.skill_model.Skill.id.in_(internship.skill_ids)).all()
        db_internship.skills.extend(skills)
        db.commit()
        db.refresh(db_internship)

    return db_internship

def get_internships(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.internship_model.Internship).offset(skip).limit(limit).all()

def get_internship_by_id(db: Session, internship_id: int):
    return db.query(models.internship_model.Internship).filter(models.internship_model.Internship.id == internship_id).first()
