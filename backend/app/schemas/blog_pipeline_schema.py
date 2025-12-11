"""Blog pipeline schema models."""

from typing import List, Optional
from pydantic import BaseModel, Field


# Blog research output
class BlogResearchOutput(BaseModel):
    topic_summary: str = Field(description="In-depth topic analysis for blog content")
    key_points: List[str] = Field(description="Comprehensive points to cover in blog")
    primary_keywords: List[str] = Field(description="Primary SEO keywords")
    secondary_keywords: List[str] = Field(description="LSI and secondary keywords")
    competitor_content_analysis: Optional[str] = Field(
        default=None, description="Analysis of competitor blog content"
    )
    seo_opportunities: List[str] = Field(description="SEO and ranking opportunities")
    content_structure_suggestions: List[str] = Field(
        description="Suggested blog structure"
    )
    backlink_opportunities: List[str] = Field(
        default_factory=list, description="Potential backlink sources"
    )
    content_gaps: List[str] = Field(
        default_factory=list, description="Gaps in existing blog content"
    )


# Blog related models
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


class EngagementEstimate(BaseModel):
    """Represents an estimated engagement metric."""

    metric: str = Field(description="The engagement metric, e.g., 'likes', 'shares'")
    estimate: str = Field(description="The estimated value or range for the metric")


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


# Final outputs
class FinalBlogOutput(BaseModel):
    """The final, user-facing output for blog content."""

    final_content: str = Field(
        description="The formatted blog post, ready for publication."
    )


class EngagementEstimate(BaseModel):
    """Represents an estimated engagement metric."""

    metric: str = Field(description="The engagement metric, e.g., 'likes', 'shares'")
    estimate: str = Field(description="The estimated value or range for the metric")
