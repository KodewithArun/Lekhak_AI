from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductGet, ProductListResponse
from app.models.product import Product
from app.models.company import Company
from datetime import datetime

router = APIRouter(prefix="/products", tags=["products"])


# Create a new product
@router.post("/", response_model=ProductGet)
async def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    # Check if the company exists
    db_company = db.query(Company).filter(Company.id == product.company_id).first()
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
    db.commit()
    db.refresh(db_product)
    return db_product


# Get a list of all products
@router.get("/", response_model=ProductListResponse)
async def list_products(db: Session = Depends(get_db)):
    products = db.query(Product).all()
    return ProductListResponse(products=products)


# Get a specific product by ID
@router.get("/{product_id}", response_model=ProductGet)
async def get_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product


# get products by company id
@router.get("/company/{company_id}", response_model=ProductListResponse)
async def get_products_by_company(company_id: int, db: Session = Depends(get_db)):
    products = db.query(Product).filter(Product.company_id == company_id).all()
    return ProductListResponse(products=products)
