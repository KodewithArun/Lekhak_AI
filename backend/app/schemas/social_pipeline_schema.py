"""Social media pipeline schema models."""

from typing import Dict, List
from pydantic import BaseModel, Field


class SocialResearchOutput(BaseModel):
    platform: str = Field(
        description="The platform being researched (from Planner: linkedin, instagram, twitter, facebook)."
    )

    platform_context: str = Field(
        description="Summary of how this specific platform behaves and what users expect."
    )

    audience_intent: Dict[str, List[str]] = Field(
        description="Primary, secondary, and tertiary user motivations for this platform."
    )

    attention_triggers: Dict[str, List[str]] = Field(
        description="Elements that capture attention on this platform."
    )

    content_angles: Dict[str, Dict[str, str]] = Field(
        description="Strategic content approaches for this platform only (problem-solution, feature focus, use-cases, etc)."
    )

    credibility_signals: List[str] = Field(
        description="What increases trust for this specific platform."
    )

    format_guidelines: Dict[str, str] = Field(
        description="Formatting rules for this platform (tone, length, hashtags, structure)."
    )

    trending_hashtags: List[str] = Field(
        description="Trending hashtags relevant to the topic on this specific platform."
    )


# below are models related to social media content creation that will be refine in upcoming steps

# Social media related models
class HashtagStrategy(BaseModel):
    """Represents a category of hashtags with its list of tags."""

    category: str = Field(
        description="The category of hashtags, e.g., 'trending', 'niche'"
    )
    tags: List[str] = Field(description="A list of hashtags for this category")


class PlatformTip(BaseModel):
    """Represents a tip for a specific social media platform."""

    platform: str = Field(
        description="The social media platform, e.g., 'Instagram', 'LinkedIn'"
    )
    tip: str = Field(description="A specific tip for that platform")


class EngagementEstimate(BaseModel):
    """Represents an estimated engagement metric."""

    metric: str = Field(description="The engagement metric, e.g., 'likes', 'shares'")
    estimate: str = Field(description="The estimated value or range for the metric")


class SocialContentVariation(BaseModel):
    platform: str
    content: str
    hashtags: List[str]
    character_count: int
    hook_type: str


class SocialWriterOutput(BaseModel):
    variations: List[SocialContentVariation]
    primary_cta: str
    engagement_strategy: str
    visual_suggestions: List[str]


class SocialOptimizerOutput(BaseModel):
    final_content: List[SocialContentVariation]
    best_posting_times: List[str]
    hashtag_strategy: List[HashtagStrategy]
    ab_test_recommendations: str
    engagement_tactics: List[str]
    visual_requirements: str
    platform_specific_tips: List[PlatformTip]


# Final outputs
class FinalSocialOutput(BaseModel):
    """The final, user-facing output for social media content."""

    final_content: str = Field(
        description="The formatted social media post, including caption and hashtags."
    )
