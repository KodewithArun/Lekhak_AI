"""
Pydantic Models for Planner Agent

Defines the input and output schemas for the Planner Agent, which is responsible
for analyzing user requests, detecting greetings, requesting clarification, and
determining the appropriate content pipeline routing.
"""

from pydantic import BaseModel, Field
from typing import List, Literal, Optional


class UserRequest(BaseModel):
    """User's content creation request"""
    instruction: str = Field(description="User's natural language content request")
    tone: str = Field(default="professional", description="Content tone")


class PlannerOutput(BaseModel):
    """Planner Agent output with extracted information and execution plan"""
    
    # Interaction type
    is_greeting: bool = Field(default=False, description="True if user is just greeting or chatting, not requesting content")
    should_proceed: bool = Field(default=True, description="False if clarification is needed or greeting, True to proceed with content generation")
    
    # Core analysis
    user_query: str = Field(description="Original user query")
    topic: str = Field(default="unknown", description="Main content topic")
    
    # Pipeline decision
    pipeline_type: Literal["social", "blog", "both", "none"] = Field(description="Selected content pipeline or 'none' if clarification needed")
    platform: str = Field(default="general", description="Target platform or 'general'")
    
    # Business context (optional)
    company_name: Optional[str] = Field(default=None, description="Company/brand name if mentioned")
    products_services: List[str] = Field(default_factory=list, description="Products or services mentioned")
    target_audience: Optional[str] = Field(default=None, description="Target audience")
    requirements: List[str] = Field(default_factory=list, description="Special requirements or constraints")
    
    # Response to user
    response_message: Optional[str] = Field(default=None, description="Direct response to user for greetings or when asking for clarification")
    clarification_needed: Optional[str] = Field(default=None, description="Question to ask the user for clarification if the request is ambiguous.")
