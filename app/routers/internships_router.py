from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..config.database import get_db

router = APIRouter()

@router.post("/internships/", response_model=schemas.internship_schemas.Internship)
def create_internship(internship: schemas.internship_schemas.InternshipCreate, db: Session = Depends(get_db)):
    return crud.internship_crud.create_internship(db=db, internship=internship)

@router.get("/internships/", response_model=List[schemas.internship_schemas.Internship])
def read_internships(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    internships = crud.internship_crud.get_internships(db, skip=skip, limit=limit)
    return internships

@router.get("/internships/{internship_id}", response_model=schemas.internship_schemas.Internship)
def read_internship(internship_id: int, db: Session = Depends(get_db)):
    db_internship = crud.internship_crud.get_internship_by_id(db, internship_id=internship_id)
    if db_internship is None:
        raise HTTPException(status_code=404, detail="Internship not found")
    return db_internship
