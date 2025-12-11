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


class ProductContext(BaseModel):
    """Product/Service context from database."""

    product_id: int
    name: str
    description: str


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


# Planner output
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
        description="Primary intention/purpose of the content (educate, promote, engage, storytelling, persuade, inform, inspire, thought_leadership)",
    )
    clarification_needed: Optional[str] = Field(
        default=None,
        description="Message requesting clarification from user if should_proceed is False",
    )
    company_context: Optional[CompanyContext] = Field(
        default=None, description="Company information from database"
    )
    product_context: Optional[ProductContext] = Field(
        default=None, description="Product information from database"
    )
