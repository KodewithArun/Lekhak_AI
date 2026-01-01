from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.company import Company
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductGet, ProductListResponse

router = APIRouter()


# Create a new product
@router.post("/", response_model=ProductGet)
async def create_product(product: ProductCreate, db: AsyncSession = Depends(get_db)):
    # Check if the company exists
    result = await db.execute(select(Company).where(Company.id == product.company_id))
    db_company = result.scalar_one_or_none()
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")

    db_product = Product(
        name=product.name,
        description=product.description,
        company_id=product.company_id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow(),
    )
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


# Get a list of all products
@router.get("/", response_model=ProductListResponse)
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return ProductListResponse(products=products)


# Get a specific product by ID
@router.get("/{product_id}", response_model=ProductGet)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    db_product = result.scalar_one_or_none()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# get products by company id
@router.get("/company/{company_id}", response_model=ProductListResponse)
async def get_products_by_company(company_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.company_id == company_id))
    products = result.scalars().all()
    return ProductListResponse(products=products)
