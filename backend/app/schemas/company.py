from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CompanyBase(BaseModel):
    name: str
    industry: str
    description: str


class CompanyCreate(CompanyBase):
    pass


class CompanyGet(CompanyBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    companies: List[CompanyGet]
