"""Social media pipeline schema models."""

from typing import List
from pydantic import BaseModel, Field


# Social media research output model
class SocialResearchOutput(BaseModel):
    trending_hashtags: List[str] = Field(
        description="Hashtags currently trending or frequently used for the topic"
    )

    competitor_captions: List[str] = Field(
        description="Captions from high-performing competitor or viral posts"
    )

    viral_hooks: List[str] = Field(
        description="Opening hooks commonly used in viral posts"
    )

    platform_trends: List[str] = Field(
        description="Content formats or trends observed on each platform"
    )

    audience_preferences: List[str] = Field(
        description="Observed audience preferences per platform based on engagement patterns"
    )


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
