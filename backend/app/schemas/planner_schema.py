"""Planner schema models for AI content planning."""

from typing import Literal, Optional
from pydantic import BaseModel, Field


# Company and Product context
class CompanyContext(BaseModel):
    """Company context from database."""

    company_id: int
    name: str = Field(max_length=100)
    industry: str = Field(max_length=100)
    description: str = Field(max_length=500)
    url: str = Field(max_length=200)


class ProductContext(BaseModel):
    """Product/Service context from database."""

    product_id: int
    name: str = Field(max_length=100)
    description: str = Field(max_length=800)
    url: str = Field(max_length=200)


# User request for planning
class UserRequest(BaseModel):
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")
    company_context: Optional[CompanyContext] = Field(
        default=None, description="Company information from database"
    )
    product_context: Optional[ProductContext] = Field(
        default=None, description="Product information from database"
    )
    framework_name: Optional[str] = Field(
        default=None, description="Selected structural framework name (e.g. AIDA)"
    )


# Planner output
class PlannerOutput(BaseModel):
    should_proceed: bool = Field(
        default=True, description="True if content generation can proceed"
    )
    user_query: str = Field(
        max_length=500, description="Original user query (summarized)"
    )
    topic: str = Field(
        default="unknown", max_length=100, description="Main content topic"
    )
    pipeline_type: Literal["social", "blog", "both", "none"] = Field(
        description="Selected content pipeline"
    )
    platform: str = Field(
        default="general", max_length=50, description="Target platform"
    )
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
        max_length=200,
        description="Message requesting clarification from user if should_proceed is False",
    )
    company_context: Optional[CompanyContext] = Field(
        default=None, description="Company information from database"
    )
    product_context: Optional[ProductContext] = Field(
        default=None, description="Product information from database"
    )
