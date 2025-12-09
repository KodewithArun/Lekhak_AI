from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyGet, CompanyListResponse
from datetime import datetime

router = APIRouter(prefix="/companies", tags=["companies"])


# Create a new company
@router.post("/", response_model=CompanyGet)
async def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    db_company = Company(
        name=company.name,
        industry=company.industry,
        description=company.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


# Get a list of all companies
@router.get("/", response_model=CompanyListResponse)
async def list_companies(db: Session = Depends(get_db)):
    companies = db.query(Company).all()
    return CompanyListResponse(companies=companies)


# Get a specific company by ID
@router.get("/{company_id}", response_model=CompanyGet)
async def get_company(company_id: int, db: Session = Depends(get_db)):
    db_company = db.query(Company).filter(Company.id == company_id).first()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company
