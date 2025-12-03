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


# Research output for both social and blog pipelines
class ResearchOutput(BaseModel):
    """Research findings for creating professional content."""

    topic_summary: str = Field(
        description="2-4 sentence overview of the topic and company context"
    )
    key_benefits: List[str] = Field(
        description="3-6 specific benefits or value propositions"
    )
    audience_pain_points: str = Field(
        description="Clear description of problems the target audience faces"
    )
    trending_hashtags: List[str] = Field(
        default_factory=list,
        description="6-8 trending hashtags WITH # symbol (for social media only)",
    )
    content_angle: str = Field(
        description="Best approach: problem-solution, transformation, educational, thought leadership, etc."
    )
    competitor_insights: Optional[str] = Field(
        default=None, description="How competitors position similar offerings"
    )
    credibility_elements: List[str] = Field(
        default_factory=list,
        description="Proof points: stats, testimonials, results, awards, etc.",
    )


# ============================================
# SOCIAL MEDIA CONTENT CREATION SCHEMAS
# ============================================


class SocialPostVariation(BaseModel):
    """A single promotional social media post."""

    platform: str = Field(
        description="Social platform: Instagram, LinkedIn, Twitter, Facebook, etc."
    )
    hook: str = Field(description="Attention-grabbing opening line (1 line)")
    content: str = Field(
        description="Main message with company/product details (2-3 lines)"
    )
    hashtags: str = Field(
        description="Trending hashtags as single string: '#tag1 #tag2 #tag3'"
    )


class SocialWriterOutput(BaseModel):
    """Output from social media writer agent."""

    posts: List[SocialPostVariation] = Field(
        description="1 optimized promotional post for the target platform"
    )


class FinalSocialOutput(BaseModel):
    """The final, user-facing output for social media content."""

    final_content: str = Field(
        description="The formatted social media post, including hook, content, and hashtags."
    )


# ============================================
# BLOG CONTENT CREATION SCHEMAS
# ============================================


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
