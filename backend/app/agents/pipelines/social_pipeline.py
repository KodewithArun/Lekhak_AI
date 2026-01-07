"""
Social Media Content Pipeline
Sequential flow: Researcher → Writer → Optimizer
"""

from google.adk.agents import LlmAgent, SequentialAgent

from app.callbacks.json_callbacks import repair_json_after_model
from app.tools.social_search_tool import serp_platform_search
from app.core.setting import GEMINI_MODEL
from app.schemas.social_pipeline_schema import (
    SocialResearchOutput,
    SocialContentOutput,
    OptimizedContent,
)
from app.utils.loggers import get_logger
from app.prompts.social_instructions.research_instruction import (
    RESEARCH_AGENT_INSTRUCTION,
)
from app.prompts.social_instructions.writer_instruction import (
    SOCIAL_AGENT_INSTRUCTION,
)
from app.prompts.social_instructions.optimizer_instruction import (
    OPTIMIZER_AGENT_INSTRUCTION,
)

logger = get_logger("social_pipeline")

# Research agent with JSON repair callback
social_researcher = LlmAgent(
    name="social_researcher",
    model=GEMINI_MODEL,
    description="In-depth research specialist for social media content.",
    instruction=RESEARCH_AGENT_INSTRUCTION,
    tools=[serp_platform_search],
    output_schema=SocialResearchOutput,
    output_key="social_research",
    after_model_callback=repair_json_after_model,
)

# Writer agent with JSON repair callback
social_writer = LlmAgent(
    name="social_writer",
    model=GEMINI_MODEL,
    description="Generates high-quality social media content including captions, main content, hashtags, hooks, and optional CTAs based on research insights for each platform.",
    instruction=SOCIAL_AGENT_INSTRUCTION,
    output_schema=SocialContentOutput,
    output_key="social_content",
    after_model_callback=repair_json_after_model,
)

# Optimizer agent with JSON repair callback
social_optimizer = LlmAgent(
    name="social_optimizer",
    model=GEMINI_MODEL,
    description="Takes AI-generated social media content and optimizes it to be human-like, engaging, and platform-ready with trending hashtags, captions, and optional hooks/CTAs based on platform conventions.",
    instruction=OPTIMIZER_AGENT_INSTRUCTION,
    output_schema=OptimizedContent,
    output_key="optimized_social_content",
    after_model_callback=repair_json_after_model,
)

social_pipeline_agent = SequentialAgent(
    name="social_pipeline",
    description="Your task is to create optimized social media content through a structured pipeline involving research, writing, and optimization stages.",
    sub_agents=[social_researcher, social_writer, social_optimizer],
)
logger.info("Social pipeline initialized with JSON repair callbacks")
