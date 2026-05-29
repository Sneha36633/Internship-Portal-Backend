from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..config.database import get_db

router = APIRouter()

@router.post("/skills/", response_model=schemas.skill_schemas.Skill)
def create_skill(skill: schemas.skill_schemas.SkillCreate, db: Session = Depends(get_db)):
    db_skill = crud.skill_crud.get_skill_by_name(db, name=skill.name)
    if db_skill:
        raise HTTPException(status_code=400, detail="Skill already exists")
    return crud.skill_crud.create_skill(db=db, skill=skill)

@router.get("/skills/", response_model=List[schemas.skill_schemas.Skill])
def read_skills(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    skills = crud.skill_crud.get_skills(db, skip=skip, limit=limit)
    return skills
