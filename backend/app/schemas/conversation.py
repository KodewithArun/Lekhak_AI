from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class ConversationBase(BaseModel):
    user_query: str
    generated_content: str


class ConversationCreate(ConversationBase):
    company_id: int
    product_id: Optional[int] = None


class ConversationGet(ConversationBase):
    id: int
    company_id: int
    product_id: Optional[int] = None
    user_id: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationListResponse(BaseModel):
    conversations: List[ConversationGet]
