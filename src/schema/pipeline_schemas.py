from typing import List, Optional
from pydantic import BaseModel, Field


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


# output schemas for various pipeline stages (later chaged based on each respective agent's output)
class ResearchOutput(BaseModel):
    topic_summary: str = Field(description="Brief topic overview")
    key_points: List[str] = Field(description="Main points to cover in content")
    keywords: List[str] = Field(description="Primary and secondary keywords")
    target_audience_insights: str = Field(description="Audience insights")
    competitor_insights: Optional[str] = Field(default=None)
    trending_topics: List[str] = Field(default_factory=list)
    data_sources: List[str] = Field(default_factory=list)
    content_gaps: List[str] = Field(default_factory=list)


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


class BlogSection(BaseModel):
    heading: str
    content: str
    key_points: List[str]


class BlogWriterOutput(BaseModel):
    headline: str
    subheadline: Optional[str] = None
    meta_description: str
    introduction: str
    sections: List[BlogSection]
    conclusion: str
    word_count: int
    reading_time: str
    key_takeaways: List[str]
    internal_links: List[str] = []
    external_sources: List[str] = []
    image_suggestions: List[str] = []


class SEOOptimization(BaseModel):
    primary_keyword: str
    secondary_keywords: List[str]
    lsi_keywords: List[str]
    keyword_density: float
    featured_snippet_opportunity: Optional[str] = None
    schema_markup: Optional[str] = None


class ReadabilityMetrics(BaseModel):
    flesch_score: Optional[float] = None
    grade_level: Optional[str] = None
    avg_sentence_length: Optional[float] = None
    improvements: List[str]


class BlogOptimizerOutput(BaseModel):
    final_headline: str
    final_meta_description: str
    optimized_content: str
    seo_optimization: SEOOptimization
    readability_metrics: ReadabilityMetrics
    image_alt_texts: List[str]
    conversion_elements: List[str]
    publication_checklist: List[str]
    estimated_engagement: List[EngagementEstimate]


class FinalSocialOutput(BaseModel):
    """The final, user-facing output for social media content."""

    final_content: str = Field(
        description="The formatted social media post, including caption and hashtags."
    )


class FinalBlogOutput(BaseModel):
    """The final, user-facing output for blog content."""

    final_content: str = Field(
        description="The formatted blog post, ready for publication."
    )
