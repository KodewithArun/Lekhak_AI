"""Planner schema models for AI content planning."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


# Company and Product context
class CompanyContext(BaseModel):
    """Company context from database."""

    company_id: int
    name: str
    industry: str
    description: str
    url: str


class ProductContext(BaseModel):
    """Product/Service context from database."""

    product_id: int
    name: str
    description: str
    url: str


# User request for planning
class UserRequest(BaseModel):
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")
    framework_name: Optional[str] = Field(
        default=None, description="Selected structural framework name (e.g. AIDA)"
    )


# Planner output
class PlannerOutput(BaseModel):
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
    platform: str = Field(default="linkedin", description="Target platform")
    tone: str = Field(description="Selected tone for content generation")
    content_intention: Literal[
        "educate",
        "promote",
        "engage",
        "storytelling",
        "persuade",
        "inform",
        "inspire",
        "thought_leadership",
    ] = Field(
        default="inform",
        description="Primary intention/purpose of the content",
    )
    clarification_needed: Optional[str] = Field(
        default=None,
        description="Message requesting clarification from user if should_proceed is False",
    )
