"""
Blog Content Pipeline
Sequential flow: Researcher → Writer → Optimizer → Presenter
"""

from google.adk.agents import SequentialAgent, LlmAgent
from src.schema.pipeline_schemas import (
    ResearchOutput,
    BlogWriterOutput,
    BlogOptimizerOutput,
    FinalBlogOutput,
)
from src.config import GEMINI_MODEL
from src.utils.loggers import get_logger

logger_blog = get_logger("blog_pipeline")

blog_researcher = LlmAgent(
    name="blog_researcher",
    model=GEMINI_MODEL,
    description="Deep research specialist for long-form blog content.",
    output_schema=ResearchOutput,
    output_key="blog_research",
    instruction="You are a blog research specialist. Based on the planner_output, conduct comprehensive research on topic depth, SEO keywords, competitor gaps, and data sources.",
)

blog_writer = LlmAgent(
    name="blog_writer",
    model=GEMINI_MODEL,
    description="Creates comprehensive, SEO-optimized blog articles.",
    output_schema=BlogWriterOutput,
    output_key="blog_content",
    instruction="You are an expert blog writer. Using the blog_research, create a comprehensive blog post with a compelling headline, structured body, and strong CTA. Target 1500-2500 words.",
)

blog_optimizer = LlmAgent(
    name="blog_optimizer",
    model=GEMINI_MODEL,
    description="Optimizes blog content for SEO and readability.",
    output_schema=BlogOptimizerOutput,
    output_key="optimized_blog_content",
    instruction="You are a blog SEO expert. Review the blog_content and optimize it. For 'estimated_engagement', provide a list of objects with 'metric' and 'estimate'.",
)

blog_presenter = LlmAgent(
    name="blog_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized blog content for the user.",
    output_schema=FinalBlogOutput,
    output_key="final_blog_post",
    instruction="You are a blog formatter. Take the optimized blog content and assemble it into a professional, well-formatted post using markdown. Exclude all internal SEO or readability metrics.",
)

blog_pipeline_agent = SequentialAgent(
    name="blog_pipeline",
    description="Complete blog content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[blog_researcher, blog_writer, blog_optimizer, blog_presenter],
)
logger_blog.info("Blog pipeline initialized")
