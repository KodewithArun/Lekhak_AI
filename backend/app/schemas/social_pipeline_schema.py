"""Social media pipeline schema models."""

from typing import List, Optional
from pydantic import BaseModel, Field


class SourceReference(BaseModel):
    """Model for source references (credibility signals, quotes, case studies)."""

    claim: str = Field(description="The statement, quote, or case study")
    value: Optional[str] = Field(
        default=None,
        description="The specific metric (e.g., '72%', '3x') if applicable",
    )
    source: Optional[str] = Field(
        default=None, description="The source name or publication"
    )
    url: Optional[str] = Field(default=None, description="URL for verification")


# Nested models for SocialResearchOutput
class AudienceIntent(BaseModel):
    primary: List[str] = Field(description="Primary audience intent")
    secondary: List[str] = Field(description="Secondary audience intent")
    tertiary: List[str] = Field(description="Tertiary audience intent")


class AttentionTriggers(BaseModel):
    problem_awareness: List[str] = Field(description="Problem awareness triggers")
    novelty: List[str] = Field(description="Novelty triggers")
    credibility: List[str] = Field(description="Credibility triggers")
    solution_relevance: List[str] = Field(description="Solution relevance triggers")
    benefit_orientation: List[str] = Field(description="Benefit orientation triggers")


class ContentAngles(BaseModel):
    thought_leadership: str = Field(description="Challenging the status quo")
    use_case_scenarios: str = Field(description="Real-world application")
    feature_deep_dive: str = Field(description="Technical exploration")
    benefit_highlight: str = Field(description="Emotional/practical benefit")
    problem_solution: str = Field(description="Direct problem solving")


class FormatGuidelines(BaseModel):
    tone: str = Field(description="Tone of the content")
    length: str = Field(description="Length guidelines")
    hashtags: str = Field(description="Hashtag strategy")
    engagement_style: str = Field(description="Engagement style")


class CompetitorInsight(BaseModel):
    """Model for competitor content analysis."""

    competitor_name: Optional[str] = Field(
        default=None, description="Name of the competitor or similar company"
    )
    content_type: Optional[str] = Field(
        default=None, description="Type of content (post, article, video, etc.)"
    )
    key_insight: Optional[str] = Field(
        default=None, description="What's working for them"
    )
    engagement_indicator: Optional[str] = Field(
        default=None,
        description="Engagement metrics if available (likes, shares, comments)",
    )
    url: Optional[str] = Field(
        default=None, description="URL to the competitor content"
    )


class TimingContext(BaseModel):
    """Model for timing and seasonality insights."""

    trending_now: Optional[List[str]] = Field(
        default=None, description="Topics trending RIGHT NOW in the industry"
    )
    seasonal_opportunities: Optional[List[str]] = Field(
        default=None, description="Seasonal hooks or timely angles"
    )
    news_hooks: Optional[List[str]] = Field(
        default=None, description="Recent news or events to tie into"
    )


class AudiencePersona(BaseModel):
    """Model for audience persona segmentation."""

    persona_name: Optional[str] = Field(
        default=None,
        description="Name of the persona (e.g., 'Startup Founder', 'Marketing Manager')",
    )
    pain_points: Optional[List[str]] = Field(
        default=None, description="Specific pain points for this persona"
    )
    motivations: Optional[List[str]] = Field(
        default=None, description="What drives this persona"
    )
    preferred_content_style: Optional[str] = Field(
        default=None, description="How this persona prefers to consume content"
    )


class SocialResearchOutput(BaseModel):
    """
    Deep research output used by the Social Content Agent.
    Designed to be extremely detailed, structured, and actionable.
    """

    platform: str = Field(
        description="The selected platform exactly as given by the Planner Agent."
    )

    platform_context: str = Field(
        description="Clear explanation of how this platform behaves, its culture, user expectations, and content norms."
    )

    audience_intent: AudienceIntent = Field(
        description="Deeply researched audience motivations. Must include primary, secondary, tertiary."
    )

    attention_triggers: AttentionTriggers = Field(
        description="Psychological triggers that attract attention on this platform."
    )

    content_angles: ContentAngles = Field(
        description="High-value content strategies with a description for each."
    )

    credibility_signals: List[SourceReference] = Field(
        description="Credibility factors like quotes, case studies, expert statements with source attribution."
    )

    statistical_claims: List[SourceReference] = Field(
        default_factory=list,
        description="List of statistical claims with source attribution.",
    )

    format_guidelines: FormatGuidelines = Field(
        description="Platform formatting rules: tone, length, hashtags, engagement style."
    )

    trending_hashtags: List[str] = Field(
        description="Relevant trending hashtags for this platform, topic-specific."
    )

    competitor_insights: Optional[List[CompetitorInsight]] = Field(
        default=None,
        description="Analysis of competitor content and what's working in the industry.",
    )

    timing_context: Optional[TimingContext] = Field(
        default=None,
        description="Timing, seasonality, and trending topics for timely content.",
    )

    audience_personas: Optional[List[AudiencePersona]] = Field(
        default=None,
        description="Segmented audience personas with specific pain points and preferences.",
    )


# Social writing output schemas


class Hooks(BaseModel):
    primary: str = Field(description="Primary hook")
    secondary: str = Field(description="Secondary hook")
    tertiary: Optional[str] = Field(default=None, description="Tertiary hook")


class SocialContentOutput(BaseModel):
    platform: str = Field(
        description="The platform for which the content is being generated (LinkedIn, Instagram, X/Twitter, Facebook)."
    )

    caption: str = Field(
        description="A short, attention-grabbing text suitable as the caption for the platform."
    )

    main_content: str = Field(
        description="Full content body that conveys the message, storytelling, or product information, adapted to the platform."
    )

    hashtags: List[str] = Field(
        description="List of 5-15 platform-relevant hashtags, mandatory for engagement and discoverability."
    )

    hooks: Optional[Hooks] = Field(
        default=None,
        description="Structured hooks for A/B testing. Keys: primary, secondary, tertiary.",
    )

    call_to_action: Optional[str] = Field(
        default=None,
        description="Optional call-to-action, e.g., 'Learn more', 'Sign up', 'Join now'.",
    )

    source_references: Optional[List[SourceReference]] = Field(
        default=None, description="List of source references used in the content."
    )

    storytelling_framework: Optional[str] = Field(
        default=None,
        description="The storytelling framework used (PAS, AIDA, Hero's Journey, Before-After-Bridge, etc.).",
    )

    target_persona: Optional[str] = Field(
        default=None, description="Primary audience persona this content targets."
    )


#  Optimized content schema


class OptimizedContent(BaseModel):
    platform: str = Field(
        description="The social media platform for this content (e.g., LinkedIn, Instagram, X/Twitter, Facebook)."
    )

    caption: str = Field(
        description="A concise, catchy line to hook the audience."
    )

    content: str = Field(
        description="The fully assembled post BODY. DO NOT include the hook/caption, CTA, or Hashtags here as they are provided in separate fields."
    )

    hashtags: List[str] = Field(
        description="A list of platform-relevant and trending hashtags for discoverability."
    )

    cta: Optional[str] = Field(
        default=None,
        description="Optional call-to-action to encourage user engagement or conversion.",
    )

    hooks: Optional[Hooks] = Field(
        default=None,
        description="Structured hooks for A/B testing (Primary = Variant A, Secondary = Variant B).",
    )

    sources: Optional[List[SourceReference]] = Field(
        default=None,
        description="List of source references preserved from writer output.",
    )

    readability_score: Optional[str] = Field(
        default=None,
        description="Readability assessment (e.g., 'Grade 7 - Easy to read', 'Grade 9 - Moderate').",
    )

    engagement_prediction: Optional[str] = Field(
        default=None,
        description="Predicted engagement level (High/Medium/Low) based on content patterns.",
    )
