"""Blog pipeline schema models."""

from typing import List, Optional, Dict
from pydantic import BaseModel, Field, field_validator


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


# BlogWriter Schema Models
class BlogSubsection(BaseModel):
    heading: str = Field(
        description="H3 subheading. Introduces a sub-point within an H2 section."
    )
    content: str = Field(
        description="Content explaining the H3 sub-point. Max 1000 characters. Supports, expands, or clarifies the main H2 idea."
    )


class BlogSection(BaseModel):
    heading: str = Field(
        description="H2 section title. Clearly states the main idea this section covers and aligns with the reader’s intent."
    )
    content: str = Field(
        description="Primary content for this section. Max 3000 characters. Provides clear, helpful, and original insights."
    )
    subsections: Optional[List[BlogSubsection]] = Field(
        default=None,
        description="Optional list of H3 subsections used when the section contains multiple steps or concepts.",
    )


class BlogWriterOutput(BaseModel):

    title: str = Field(
        description="H1 blog title under 70 characters. Includes a primary keyword and communicates the main promise of the article."
    )

    meta_description: str = Field(
        description="SEO meta description (≤160 chars). Summarizes the blog’s value so users are motivated to click."
    )

    introduction: str = Field(
        description="Opening paragraph (≤2000 chars). Hooks the reader, identifies their pain point or curiosity, and explains what the blog will deliver."
    )

    sections: List[BlogSection] = Field(
        description="3–5 H2 sections forming the main body. Each section must add value and flow logically from the previous one."
    )

    conclusion: str = Field(
        description="Ending paragraph (≤1500 chars). Summarizes the post, reinforces key points, and prepares the reader for the CTA."
    )

    primary_keywords: List[str] = Field(
        description="Core SEO keywords. These must appear naturally in the title, introduction, and at least one section."
    )

    secondary_keywords: List[str] = Field(
        description="Related long-tail keywords used naturally throughout the content to improve search relevance."
    )

    data_backed_claims: List[str] = Field(
        description="2–3 verified facts or statistics included in the article to increase credibility and trust."
    )

    unique_angle: str = Field(
        description="What makes this blog different from competitors (e.g., new insight, missing perspective, or improved explanation)."
    )

    content_format: str = Field(
        description="The chosen structure for the blog, such as 'how-to', 'listicle', 'conversational', 'problem-solution', 'interview', or 'infographic-style'."
    )

    target_audience: str = Field(
        description="The specific reader the blog is written for (e.g., beginners, marketers, founders, students)."
    )

    tone: str = Field(
        description="The writing voice used in the blog (e.g., friendly, expert, conversational, direct, or authoritative)."
    )

    word_count: int = Field(
        ge=800,
        le=2000,
        description="Total length of the article. Must stay between 800–2000 words for readability and SEO value.",
    )

    cta_text: str = Field(
        description="The exact call-to-action shown in the conclusion (e.g., 'Download the guide', 'Try the tool', 'Learn more')."
    )

    sources: Optional[List[str]] = Field(
        default=None,
        description="Optional list of URLs used to verify claims, statistics, or research references.",
    )


# optimizer output
class OptimizedHeading(BaseModel):
    old: str = Field(description="Original H2/H3 heading from the draft.")
    new: str = Field(description="Improved, clearer, and more engaging heading.")
    reason: str = Field(
        description="Why this change improves readability, structure, or SEO."
    )


class ContentFix(BaseModel):
    issue: str = Field(description="Specific content or structure problem detected.")
    suggestion: str = Field(description="Actionable guidance to fix the issue.")
    section_reference: str = Field(
        description="Section or H3 heading where the fix applies."
    )


class SEOImprovement(BaseModel):
    type: str = Field(
        description="SEO aspect to improve (title, meta, keyword usage, linking)."
    )
    suggestion: str = Field(description="Qualitative instruction for better SEO.")
    impact: str = Field(
        description="Explanation of benefit for SEO or user experience."
    )


class BlogOptimizerOutput(BaseModel):
    final_title: Optional[str] = Field(
        description="Refined, keyword-focused, human-friendly title."
    )
    final_meta_description: Optional[str] = Field(
        description="Improved meta description under 160 characters."
    )
    final_content: str = Field(
        description="The complete, optimized, and polished blog content ready for publication."
    )
    structural_fixes: List[ContentFix] = Field(
        description="List of actionable content or structure fixes applied."
    )
    heading_improvements: List[OptimizedHeading] = Field(
        description="Improvements made to H2/H3 headings."
    )
    seo_suggestions: List[SEOImprovement] = Field(
        description="SEO enhancements applied to the content."
    )
    missing_elements: List[str] = Field(
        description="High-value elements added (examples, case studies, stats)."
    )
    tone_adjustments: str = Field(
        description="Adjustments made to match audience tone and sound human."
    )
    cta_improvement: str = Field(description="Enhancements made to the call-to-action.")
    summary_of_changes: str = Field(
        description="Concise summary of main improvements made."
    )
    references_for_verification: List[str] = Field(
        description="List of all verified source URLs used in the content."
    )
