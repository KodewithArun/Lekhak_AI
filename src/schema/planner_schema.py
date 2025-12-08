from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class CompanyContext(BaseModel):
    """Company context from database."""

    company_id: int
    name: str
    industry: str
    description: str
    target_audience: str
    brand_voice: str


class ProductContext(BaseModel):
    """Product/Service context from database."""

    product_id: int
    name: str
    description: str
    key_features: str


class UserRequest(BaseModel):
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")
    company_context: Optional[CompanyContext] = Field(
        default=None, description="Company information from database"
    )
    product_context: Optional[ProductContext] = Field(
        default=None, description="Product information from database"
    )


class PlannerOutput(BaseModel):
    should_proceed: bool = Field(
        default=True, description="True if content generation can proceed"
    )
    user_query: str = Field(description="Original user query")
    topic: str = Field(default="unknown", description="Main content topic")
    pipeline_type: Literal["social", "blog", "both", "none"] = Field(
        description="Selected content pipeline"
    )
    platform: str = Field(default="general", description="Target platform")
    company_context: Optional[CompanyContext] = Field(
        default=None, description="Company information from database"
    )
    product_context: Optional[ProductContext] = Field(
        default=None, description="Product information from database"
    )
    requirements: List[str] = Field(
        default_factory=list, description="Specific requirements or requests"
    )
    clarification_needed: Optional[str] = Field(
        default=None, description="Question if more info is needed"
    )
