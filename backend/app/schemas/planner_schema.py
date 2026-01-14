"""Planner schema models for AI content planning."""

from typing import Literal, Optional
from pydantic import Field

from app.schemas.base import StrictSchema


# Company and Product context
class CompanyContext(StrictSchema):
    """Company context from database."""

    company_id: int
    name: str
    industry: str
    description: str
    url: str


class ProductContext(StrictSchema):
    """Product/Service context from database."""

    product_id: int
    name: str
    description: str
    url: str


# User request for planning
class UserRequest(StrictSchema):
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")
    framework_name: Optional[str] = Field(
        default=None, description="Selected structural framework name (e.g. AIDA)"
    )


# Planner output
class PlannerOutput(StrictSchema):
    should_proceed: bool = Field(
        default=True, description="True if content generation can proceed"
    )
    user_query: str = Field(description="Original user query (summarized)")
    topic: str = Field(
        description="Main topic of the content by understanding user query"
    )
    pipeline_type: Literal["social", "blog", "both", "none"] = Field(
        description="Selected content pipeline"
    )
    platform: str = Field(default="linkedin", description="Target platform (e.g. linkedin, twitter, blog)")
    tone: str = Field(description="Selected tone for content generation")
    clarification_needed: Optional[str] = Field(
        default=None,
        description="Message requesting clarification from user if should_proceed is False",
    )
