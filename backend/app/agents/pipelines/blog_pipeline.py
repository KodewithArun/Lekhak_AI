"""
Blog Content Pipeline
Sequential flow: Researcher → Writer → Optimizer → Presenter

This pipeline uses Google ADK (Generative AI SDK) with function calling
to create SEO-optimized blog content for product marketing.
"""

from google.adk.agents import SequentialAgent, LlmAgent
from app.core.setting import GEMINI_MODEL
from app.schemas.blog_pipeline_schema import (
    BlogOptimizerOutput,
    BlogResearchOutput,
    BlogWriterOutput,
    FinalBlogOutput,
)
from app.tools.blog_tool import serp_google_search
from app.prompts.blog_instruction.blog_research_instruction import (
    blog_research_instruction,
)
from app.prompts.blog_instruction.blog_writer_instruction import (
    blog_writer_instruction,
)
from app.prompts.blog_instruction.blog_optimizer_instruction import (
    blog_optimizer_instruction,
)

from app.utils.loggers import get_logger


logger_blog = get_logger("blog_pipeline")


blog_researcher = LlmAgent(
    name="blog_researcher",
    model=GEMINI_MODEL,
    description=(
        "Senior Content Strategist & Researcher. "
        "Responsible for conducting deep, multi-step research to find "
        "statistics, user personas, search intent, and competitor gaps. "
        "Uses SERP data to build a comprehensive foundation for high-quality blog content."
    ),
    instruction=blog_research_instruction,
    tools=[serp_google_search],
    output_schema=BlogResearchOutput,
    output_key="blog_research",
)


blog_writer = LlmAgent(
    name="blog_writer",
    model=GEMINI_MODEL,
    description="Transforms strategic research insights into a structured, SEO-optimized, and audience-focused blog post. Generates human-quality content that fills competitor gaps, incorporates verified data, and follows proven best practices for engagement and readability.",
    output_schema=BlogWriterOutput,
    instruction=blog_writer_instruction,
    output_key="blog_writer",
)

blog_optimizer = LlmAgent(
    name="blog_optimizer",
    model=GEMINI_MODEL,
    description="Refines draft blog content into polished, human-sounding posts that are SEO-optimized, easy to read, and aligned with audience intent",
    instruction=blog_optimizer_instruction,
    output_schema=BlogOptimizerOutput,
    output_key="blog_optimizer",
)

blog_presenter = LlmAgent(
    name="blog_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized blog content for the user.",
    output_schema=FinalBlogOutput,
    output_key="blog_final_output",
    instruction="Format optimized blog into professional, well-structured post with markdown. Exclude internal SEO/readability metrics. Ready-to-publish format.",
)

blog_pipeline_agent = SequentialAgent(
    name="blog_pipeline",
    description="Complete blog content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[blog_researcher, blog_writer, blog_optimizer, blog_presenter],
)
logger_blog.info("Blog pipeline initialized")
