"""Blog pipeline schema models."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field


# for keyword research
class KeywordResearch(BaseModel):
    primary_keywords: List[str] = Field(
        description="Primary SEO keywords extracted from SERP data"
    )
    secondary_keywords: List[str] = Field(
        description="Secondary SEO keywords from related searches and competitor data"
    )
    long_tail_keywords: List[str] = Field(
        description="Long-tail keywords from People Also Ask and related searches"
    )


# for competitor research
class CompetitorResearch(BaseModel):
    competitor_names: List[str] = Field(
        description="Competitor or alternative product/service names found in SERP results"
    )
    competitor_gaps: List[str] = Field(
        description="Important topics or user questions competitors do NOT cover well"
    )


# for pain point analysis
class PainPointAnalysis(BaseModel):
    pain_points: List[str] = Field(
        description="List of user pain points derived from product features and target audience"
    )


# blog research output
class BlogResearchOutput(BaseModel):
    keyword_research: KeywordResearch
    competitor_research: CompetitorResearch
    pain_point_analysis: PainPointAnalysis

    sources: List[str] = Field(
        description="SERP URLs used for research and data collection"
    )


class BlogSection(BaseModel):
    heading: Optional[str] = None
    content: Optional[str] = None
    key_points: List[str] = []


class BlogWriterOutput(BaseModel):
    headline: Optional[str] = None
    meta_description: Optional[str] = None
    introduction: Optional[str] = None
    sections: List[BlogSection] = []
    conclusion: Optional[str] = None


class SEOOptimization(BaseModel):
    primary_keyword: Optional[str] = None
    secondary_keywords: List[str] = []
    lsi_keywords: List[str] = []
    keyword_density: Optional[float] = None


class ReadabilityMetrics(BaseModel):
    flesch_score: Optional[float] = None
    grade_level: Optional[str] = None
    avg_sentence_length: Optional[float] = None
    improvements: List[str] = []


class BlogOptimizerOutput(BaseModel):
    final_headline: Optional[str] = None
    final_meta_description: Optional[str] = None
    optimized_content: Optional[str] = None
    seo_optimization: Optional[SEOOptimization] = None
    readability_metrics: Optional[ReadabilityMetrics] = None
    image_alt_texts: List[str] = []
    conversion_elements: List[str] = []
    publication_checklist: List[str] = []


# Final outputs
class FinalBlogOutput(BaseModel):
    """The final, user-facing output for blog content."""

    final_content: str = Field(
        description="The formatted blog post, ready for publication."
    )
