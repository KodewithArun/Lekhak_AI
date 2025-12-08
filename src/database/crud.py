"""CRUD functions for database operations."""

from typing import List, Optional
from sqlalchemy.orm import Session
from src.database.models import Company, Product, Conversation


# ==================== COMPANY FUNCTIONS ====================


def create_company(db: Session, name: str, industry: str, description: str) -> Company:
    """Create a new company."""
    company = Company(name=name, industry=industry, description=description)
    db.add(company)
    db.commit()
    db.refresh(company)
    return company


def get_company_by_id(db: Session, company_id: int) -> Optional[Company]:
    """Get company by ID."""
    return db.query(Company).filter(Company.id == company_id).first()


def get_all_companies(db: Session) -> List[Company]:
    """Get all companies."""
    return db.query(Company).all()


def update_company(db: Session, company_id: int, **kwargs) -> Optional[Company]:
    """Update company."""
    company = get_company_by_id(db, company_id)
    if company:
        for key, value in kwargs.items():
            if hasattr(company, key) and value is not None:
                setattr(company, key, value)
        db.commit()
        db.refresh(company)
    return company


def delete_company(db: Session, company_id: int) -> bool:
    """Delete company."""
    company = get_company_by_id(db, company_id)
    if company:
        db.delete(company)
        db.commit()
        return True
    return False


# ==================== PRODUCT FUNCTIONS ====================


def create_product(
    db: Session, company_id: int, name: str, description: str, key_features: str
) -> Product:
    """Create a new product."""
    product = Product(
        company_id=company_id,
        name=name,
        description=description,
        key_features=key_features,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def get_product_by_id(db: Session, product_id: int) -> Optional[Product]:
    """Get product by ID."""
    return db.query(Product).filter(Product.id == product_id).first()


def get_products_by_company(db: Session, company_id: int) -> List[Product]:
    """Get all products for a company."""
    return db.query(Product).filter(Product.company_id == company_id).all()


def update_product(db: Session, product_id: int, **kwargs) -> Optional[Product]:
    """Update product."""
    product = get_product_by_id(db, product_id)
    if product:
        for key, value in kwargs.items():
            if hasattr(product, key) and value is not None:
                setattr(product, key, value)
        db.commit()
        db.refresh(product)
    return product


def delete_product(db: Session, product_id: int) -> bool:
    """Delete product."""
    product = get_product_by_id(db, product_id)
    if product:
        db.delete(product)
        db.commit()
        return True
    return False


# ==================== CONVERSATION FUNCTIONS ====================


def create_conversation(
    db: Session,
    company_id: int,
    user_query: str,
    generated_content: str,
    product_id: Optional[int] = None,
) -> Conversation:
    """Create a new conversation record."""
    conversation = Conversation(
        company_id=company_id,
        product_id=product_id,
        user_query=user_query,
        generated_content=generated_content,
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def save_conversation(
    company_id: int,
    user_query: str,
    generated_content: str,
    product_id: Optional[int] = None,
) -> Conversation:
    """Save conversation to database with automatic session management."""
    from src.database import SessionLocal

    db = SessionLocal()
    try:
        conversation = create_conversation(
            db,
            company_id=company_id,
            user_query=user_query,
            generated_content=generated_content,
            product_id=product_id,
        )
        return conversation
    finally:
        db.close()
