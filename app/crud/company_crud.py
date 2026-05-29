from sqlalchemy.orm import Session
from .. import models, schemas

def create_company(db: Session, company: schemas.company_schemas.CompanyCreate):
    db_company = models.company_model.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company

def get_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.company_model.Company).offset(skip).limit(limit).all()
