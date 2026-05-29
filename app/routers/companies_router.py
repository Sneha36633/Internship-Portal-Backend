from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from .. import crud, schemas
from ..config.database import get_db

router = APIRouter()

@router.post("/companies/", response_model=schemas.company_schemas.Company)
def create_company(company: schemas.company_schemas.CompanyCreate, db: Session = Depends(get_db)):
    return crud.company_crud.create_company(db=db, company=company)

@router.get("/companies/", response_model=List[schemas.company_schemas.Company])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = crud.company_crud.get_companies(db, skip=skip, limit=limit)
    return companies
