from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.company import Company
from app.schemas.company import CompanyCreate, CompanyGet, CompanyListResponse

router = APIRouter()


# Create a new company
@router.post("/", response_model=CompanyGet)
async def create_company(company: CompanyCreate, db: AsyncSession = Depends(get_db)):
    db_company = Company(
        name=company.name,
        industry=company.industry,
        description=company.description,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_company)
    await db.commit()
    await db.refresh(db_company)
    return db_company


# Get a list of all companies
@router.get("/", response_model=CompanyListResponse)
async def list_companies(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company))
    companies = result.scalars().all()
    return CompanyListResponse(companies=companies)


# Get a specific company by ID
@router.get("/{company_id}", response_model=CompanyGet)
async def get_company(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Company).where(Company.id == company_id))
    db_company = result.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    return db_company
