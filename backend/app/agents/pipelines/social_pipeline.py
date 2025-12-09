"""
Social Media Content Pipeline
Sequential flow: Researcher: Writer : Optimizer : Presenter
"""

from google.adk.agents import SequentialAgent, LlmAgent
from app.schemas.social_pipeline_schema import (
    SocialResearchOutput,
    SocialWriterOutput,
    SocialOptimizerOutput,
    FinalSocialOutput,
)
from app.core.setting import GEMINI_MODEL
from app.utils.loggers import get_logger

logger = get_logger("social_pipeline")

social_researcher = LlmAgent(
    name="social_researcher",
    model=GEMINI_MODEL,
    description="Researches topics for social media.",
    output_schema=SocialResearchOutput,
    output_key="social_research",
    instruction="You are a social media research specialist. Based on the planner_output, research trends, engagement strategies, hashtags, competitor content, and audience pain points.",
)

social_writer = LlmAgent(
    name="social_writer",
    model=GEMINI_MODEL,
    description="Creates engaging social media content.",
    output_schema=SocialWriterOutput,
    output_key="social_content",
    instruction="You are an expert social media writer. Using the social_research, create compelling content with hooks, platform-appropriate formatting, hashtags, and CTAs. Generate 2-3 variations.",
)

social_optimizer = LlmAgent(
    name="social_optimizer",
    model=GEMINI_MODEL,
    description="Optimizes social content for engagement.",
    output_schema=SocialOptimizerOutput,
    output_key="optimized_social_content",
    instruction="You are a social media optimization expert. Review the social_content and optimize it. For 'hashtag_strategy', provide a list of objects with 'category' and 'tags'. For 'platform_specific_tips', provide a list of objects with 'platform' and 'tip'.",
)

social_presenter = LlmAgent(
    name="social_presenter",
    model=GEMINI_MODEL,
    description="Formats the optimized social content for the user.",
    output_schema=FinalSocialOutput,
    output_key="final_social_post",
    instruction="""
        You are a content formatter. Your task is to take the optimized social media content and present it cleanly to the user.

    Here is the optimized data: {optimized_social_content}

    The data contains a list of social media posts. Your job is to format this list into a single, easy-to-read string.
    For EACH post in the list, create a separate section with the platform name, the content, and the hashtags.

    Do not include any other internal strategy. Just format the posts.

    Example format:
     Platform: Twitter 
    [The text of the post goes here]

    Hashtags: #tag1 #tag2 #tag3

     Platform: LinkedIn 
    [The text of the post goes here]

    Hashtags: #tag1 #tag2 #tag3
    """,
)

social_pipeline_agent = SequentialAgent(
    name="social_pipeline",
    description="Complete social media content creation pipeline. Flow: Research → Write → Optimize → Present",
    sub_agents=[social_researcher, social_writer, social_optimizer, social_presenter],
)
logger.info("Social pipeline initialized")
