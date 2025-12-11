from datetime import datetime
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=True)
    user_query = Column(String, nullable=False)
    generated_content = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    company = relationship("Company", back_populates="conversations")
    product = relationship("Product", back_populates="conversations")

    def __repr__(self):
        return (
            f"<Conversation(id={self.id}, company_id={self.company_id}, "
            f"product_id={self.product_id})>"
        )
