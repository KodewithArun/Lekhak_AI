from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")


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
    company_name: Optional[str] = Field(
        default=None, description="Company name if mentioned"
    )
    products_services: List[str] = Field(
        default_factory=list, description="Products or services mentioned"
    )
    target_audience: Optional[str] = Field(default=None, description="Target audience")
    requirements: List[str] = Field(
        default_factory=list, description="Specific requirements"
    )
    clarification_needed: Optional[str] = Field(
        default=None, description="Question if more info is needed"
    )
