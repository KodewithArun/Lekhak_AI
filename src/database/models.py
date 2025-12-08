"""Database models for Lekhak AI."""

from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from src.database.session import Base


class Company(Base):
    """Company/Organization table."""

    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(100), nullable=False)
    description = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    products = relationship(
        "Product", back_populates="company", cascade="all, delete-orphan"
    )
    conversations = relationship(
        "Conversation", back_populates="company", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"<Company(id={self.id}, name='{self.name}', industry='{self.industry}')>"
        )


class Product(Base):
    """Product/Service table."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    key_features = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationship
    company = relationship("Company", back_populates="products")

    def __repr__(self):
        return (
            f"<Product(id={self.id}, name='{self.name}', company_id={self.company_id})>"
        )


class Conversation(Base):
    """Conversation/Content generation history table."""

    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    user_query = Column(Text, nullable=False)
    generated_content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationship
    company = relationship("Company", back_populates="conversations")

    def __repr__(self):
        return f"<Conversation(id={self.id}, company_id={self.company_id})>"
