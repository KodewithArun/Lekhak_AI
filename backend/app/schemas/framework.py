from typing import Optional
from pydantic import BaseModel

class FrameworkBase(BaseModel):
    name: str
    description: Optional[str] = None
    instruction: str


class FrameworkCreate(FrameworkBase):
    pass

class FrameworkResponse(FrameworkBase):
    id: int

    class Config:
        from_attributes = True
