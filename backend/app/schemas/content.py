"""Content generation API schemas."""

from typing import Optional
from pydantic import BaseModel, Field


class ContentRequest(BaseModel):
    prompt: str
    user_id: str = Field(
        default="default_user", description="User ID for session management"
    )
    session_id: Optional[str] = Field(
        default=None, description="Unique session/task ID for content isolation"
    )
    company_id: int = Field(description="Company ID - required for all content generation")
    product_id: Optional[int] = Field(
        default=None, 
        description="Product ID - optional when using company as product"
    )
    framework_id: Optional[int] = Field(default=None, description="Framework ID (optional - defaults to AIDA)")
    tone: str = Field(default="professional", description="Content tone (e.g., professional, casual, friendly)")
    use_company_as_product: bool = Field(
        default=False,
        description="If True and product_id is not provided, use company information as product context (useful when company name = product name, e.g., Google)",
    )


class ContentResponse(BaseModel):
    content: str
    company_id: int  # Required - matches request
    product_id: Optional[int] = None
    user_query: str
    generated_at: str  # ISO format datetime
    conversation_id: Optional[int] = None  # ID of saved conversation


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
