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
    """Research findings for creating professional content.

    This schema captures structured research insights that content writers will use.
    All fields should contain SPECIFIC, FACTUAL information from research, not generic statements.
    """

    topic_summary: str = Field(
        description="""2-4 sentence overview combining:
        1) What the topic is and why it matters
        2) How the company/product relates to this topic
        3) Key context the audience needs to know
        
        Example: 'AI-powered task management helps teams reduce meeting time by 30-50%. 
        TechFlow's TaskMaster Pro uses machine learning to automate daily standups for 5000+ agile teams. 
        The tool integrates with Slack, Jira, and Asana to provide instant progress insights.'
        
        NOT generic like: 'Task management is important for productivity.'"""
    )

    key_benefits: List[str] = Field(
        description="""3-6 SPECIFIC benefits or features (not generic claims).
        
        Each benefit should be concrete and actionable:
        ✓ GOOD: 'Automated daily standup reports save 10 hours per week'
        ✓ GOOD: 'Real-time Jira integration syncs tasks automatically'
        ✗ BAD: 'Improves productivity'
        ✗ BAD: 'Easy to use'
        
        Focus on measurable outcomes, specific features, or unique capabilities.""",
        min_length=3,
        max_length=8,
    )

    audience_pain_points: str = Field(
        description="""2-3 sentences describing SPECIFIC problems the target audience faces that this content addresses.
        
        Example: 'Project managers waste 5-10 hours weekly in status meetings. 
        Teams struggle to track progress across multiple tools. 
        Remote work makes it harder to know who's blocked or needs help.'
        
        NOT: 'People want to be more productive.'"""
    )

    trending_hashtags: List[str] = Field(
        default_factory=list,
        description="""6-8 trending hashtags WITH # symbol (for social media only, empty for blog).
        
        Must include the # symbol: ['#AI', '#Productivity', '#ProjectManagement']
        Mix of: trending (high reach), niche (targeted), and branded hashtags.
        
        For blogs, return empty list [].""",
        max_length=10,
    )

    content_angle: str = Field(
        description="""The strategic approach for this content. Choose ONE:
        
        - 'problem-solution': Highlight pain point, present solution
        - 'product-launch': Announce new feature/product
        - 'educational': Teach best practices or how-to
        - 'thought-leadership': Industry insights and trends
        - 'social-proof': Customer success stories
        - 'transformation': Before/after improvement story
        
        Example: 'problem-solution' for content about solving meeting overload."""
    )

    competitor_insights: Optional[str] = Field(
        default=None,
        description="""How competitors or similar products position themselves (1-2 sentences).
        
        Example: 'Competitors like Asana and Monday focus on visual boards, 
        while TaskMaster differentiates with AI-powered automation.'
        
        Leave None if no competitor research was done.""",
    )

    credibility_elements: List[str] = Field(
        default_factory=list,
        description="""Proof points that add credibility (stats, awards, testimonials, research data).
        
        Examples:
        - '5000+ teams use this tool daily'
        - 'Rated 4.8/5 on G2 with 500+ reviews'
        - 'Study shows 30% reduction in meeting time'
        - 'Featured in TechCrunch and Forbes'
        
        Only include VERIFIABLE facts from research. Empty list if none found.""",
        max_length=6,
    )


# ============================================
# SOCIAL MEDIA CONTENT CREATION SCHEMAS
# ============================================


class SocialPostVariation(BaseModel):
    """A single promotional social media post optimized for a specific platform.

    Structure: Hook (1 line) + Content (2-3 lines) + Hashtags
    """

    platform: str = Field(
        description="""Target social platform: 'LinkedIn', 'Instagram', 'Twitter', 'Facebook', etc.
        
        Must match the platform from planner_output exactly."""
    )

    hook: str = Field(
        description="""Attention-grabbing opening line (1 sentence, 10-15 words max).
        
        Purpose: Stop the scroll, make them want to read more.
        
        Techniques:
        - Question: 'What if your team could save 10 hours per week?'
        - Bold statement: 'Stop wasting time in endless standups.'
        - Surprising fact: '73% of project managers say meetings kill productivity.'
        - Emotional trigger: 'Drowning in tasks with no time to breathe?'
        
        Platform styles:
        - LinkedIn: Professional, thought-provoking
        - Instagram: Visual, emotional, aspirational
        - Twitter: Punchy, controversial, timely
        - Facebook: Relatable, conversational
        
        ✗ AVOID: Generic hooks like 'Exciting news!' or 'Check this out!'"""
    )

    content: str = Field(
        description="""Main message (2-3 sentences, 30-60 words).
        
        Must include:
        1. Company/product name naturally integrated
        2. 2-3 specific benefits from research (not generic claims)
        3. Credibility element if available (stat, social proof)
        4. Call-to-action or next step
        
        Example: 'Introducing TaskMaster Pro by TechFlow - the AI assistant that automates 
        daily standups for 5000+ agile teams. Save 30% of your meeting time and get instant 
        progress insights. Try free today → link'
        
        ✗ AVOID: 
        - Generic buzzwords ('revolutionary', 'game-changing')
        - Invented features not from research
        - Overly salesy language
        - AI-isms like 'dive into', 'unlock', 'elevate'"""
    )

    hashtags: str = Field(
        description="""Space-separated hashtags from social_research.trending_hashtags.
        
        Format: '#AI #Productivity #ProjectManagement #Agile #SaaS #Innovation'
        
        CRITICAL: Use ONLY the exact hashtags from research. Do NOT create new ones.
        Include the # symbol with each tag.
        Separate with single spaces."""
    )


class SocialWriterOutput(BaseModel):
    """Output from social media writer agent - contains the crafted post(s)."""

    posts: List[SocialPostVariation] = Field(
        description="""List containing exactly 1 optimized post for the target platform.
        
        The post should be copy-paste ready and platform-optimized.""",
        min_length=1,
        max_length=1,
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
