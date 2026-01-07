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
    company_id: Optional[int] = None
    product_id: Optional[int] = None
    framework_id: Optional[int] = None
    tone: Optional[str] = None


class ContentResponse(BaseModel):
    content: str
    company_id: Optional[int] = None
    product_id: Optional[int] = None
    user_query: str
    generated_at: str  # ISO format datetime
    conversation_id: Optional[int] = None  # ID of saved conversation


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
