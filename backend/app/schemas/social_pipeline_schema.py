"""Social media pipeline schema models."""

from typing import List, Optional
from pydantic import BaseModel, Field


# Social media research output
class SocialResearchOutput(BaseModel):
    topic_summary: str = Field(description="Brief topic overview for social media")
    key_points: List[str] = Field(description="Main points to cover in social content")
    trending_hashtags: List[str] = Field(description="Trending and relevant hashtags")
    platform_trends: List[str] = Field(description="Current platform-specific trends")
    audience_engagement_insights: str = Field(
        description="How audience engages with similar content"
    )
    viral_content_patterns: List[str] = Field(description="Patterns from viral content")
    optimal_posting_times: List[str] = Field(description="Best times to post")
    competitor_social_performance: Optional[str] = Field(
        default=None, description="How competitors perform on social"
    )
    content_gaps: List[str] = Field(
        default_factory=list, description="Gaps in current social content"
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
