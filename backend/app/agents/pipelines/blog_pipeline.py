"""
Blog Content Pipeline
Sequential flow: Researcher → Writer → Optimizer → Presenter

This pipeline uses Google ADK (Generative AI SDK) with function calling
to create SEO-optimized blog content for product marketing.
"""

from google.adk.agents import SequentialAgent, Agent
from app.core.setting import GEMINI_MODEL
from app.schemas.blog_pipeline_schema import (
    BlogOptimizerOutput,
    BlogResearchOutput,
    BlogWriterOutput,
    FinalBlogOutput,
)
from app.tools.blog_tool import (
    serp_google_search,
    extract_seo_keywords,
    analyze_pain_points,
    competitor_gap_analysis,
)
from app.prompts.blog_instruction.blog_research_instruction import (
    blog_research_instruction,
)

from app.utils.loggers import get_logger


logger_blog = get_logger("blog_pipeline")


blog_researcher = Agent(
    name="blog_researcher",
    model=GEMINI_MODEL,
    tools=[
        serp_google_search,
        extract_seo_keywords,
        analyze_pain_points,
        competitor_gap_analysis,
    ],
    description=(
        "Generative AI-powered research agent for SEO and content planning. "
        "Uses SERPAPI data to collect organic results, People Also Ask questions, "
        "related searches, and competitor information. "
        "Extracts primary, secondary, and long-tail keywords, analyzes product-related pain points, "
        "and identifies competitor content gaps. "
        "Provides structured, fact-backed insights for research and strategy purposes only."
    ),
    output_schema=BlogResearchOutput,
    output_key="blog_research",
    instruction=blog_research_instruction,
)


blog_writer = Agent(
    name="blog_writer",
    model=GEMINI_MODEL,
    description="Creates comprehensive, SEO-optimized blog articles.",
    output_schema=BlogWriterOutput,
    output_key="blog_content",
    instruction="""
Write a blog post (1500-2000 words) using research output and planner_output.

Focus on:
1) SEO Keywords - Integrate primary and secondary keywords naturally.
2) User Intent - Address informational, navigational, and transactional intent.
3) Content Structure - Use clear headings, subheadings, and bullet points.
4) Engaging Style - Maintain a conversational tone, use storytelling and examples.
5) People Also Ask - Answer relevant PAA questions from research.
6) Competitor Gaps - Cover topics competitors missed.
7) Company/Product Focus - Tailor content to specific company/product context.
8) Call to Action - End with a strong CTA aligned with content intention.

 CRITICAL CHARACTER LIMITS - STRICTLY ENFORCE:
- headline: MAX 200 chars (keep concise and punchy)
- subheadline: MAX 250 chars (optional, short description)
- meta_description: MAX 160 chars  CRITICAL - MUST be under 160!
- introduction: MAX 2000 chars (engaging opening)
- section heading: MAX 200 chars each
- section content: MAX 3000 chars each
- conclusion: MAX 1500 chars (strong closing)
- MAX 10 sections total
- MAX 5 key_takeaways
- MAX 10 internal_links
- MAX 8 external_sources
- MAX 6 image_suggestions

SPECIAL NOTE ON META DESCRIPTION:
The meta_description is EXTREMELY IMPORTANT for SEO. It MUST be:
- Between 150-160 characters (aim for 155)
- Compelling and include main keyword
- Actionable and clear
- Count every character including spaces!

IMPORTANT:
- Ensure factual accuracy based on research data.
- Stay within ALL character limits above - NO EXCEPTIONS.
- Avoid fluff; stay on topic.
""",
)

blog_optimizer = Agent(
    name="blog_optimizer",
    model=GEMINI_MODEL,
    description="Optimizes blog content for SEO and readability.",
    output_schema=BlogOptimizerOutput,
    output_key="optimized_blog_content",
    instruction="""
Optimize blog content for SEO and readability.

CRITICAL LIMITS:
- optimized_content: MAX 15,000 characters
- MAX 10 image_alt_texts
- MAX 8 conversion_elements
- MAX 10 publication_checklist items
- MAX 5 estimated_engagement metrics

Focus on:
1) Keyword placement
2) Subheading clarity
3) Content flow
4) Meta description (max 160 characters)

Be concise and stay within limits.
""",
)

blog_presenter = Agent(
    name="blog_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized blog content for the user.",
    output_schema=FinalBlogOutput,
    output_key="final_blog_post",
    instruction="Format optimized blog into professional, well-structured post with markdown. Exclude internal SEO/readability metrics. Ready-to-publish format.",
)

blog_pipeline_agent = SequentialAgent(
    name="blog_pipeline",
    description="Complete blog content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[blog_researcher, blog_writer, blog_optimizer, blog_presenter],
)
logger_blog.info("Blog pipeline initialized")
