from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, unique=True, index=True, nullable=False)
    industry = Column(String, nullable=True)
    description = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    products = relationship("Product", back_populates="company")
    conversations = relationship("Conversation", back_populates="company")

    def __repr__(self):
        return f"<Company(id={self.id}, name={self.name})>"
