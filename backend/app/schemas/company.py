from datetime import datetime
from typing import List
from pydantic import BaseModel


class CompanyBase(BaseModel):
    name: str
    industry: str
    description: str
    url: str


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
