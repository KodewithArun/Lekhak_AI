"""
Planner Agent - Analyzes user requests and determines the correct content pipeline.

This agent serves as the entry point for all user requests, handling:
- Request validation and clarification
- Content pipeline routing (blog/social/both/none)
- Context extraction (topic, platform, audience, etc.)
"""

from dotenv import load_dotenv
from google.adk.agents import Agent

from src.schema.planner_schema import UserRequest, PlannerOutput
from src.utils.loggers import get_logger
from src.prompts.planner_instruction import INSTRUCTION


load_dotenv()

logger = get_logger("planner_agent")


try:
    logger.info("Planner agent initialized")

    planner_agent = Agent(
        name="planner_agent",
        model="gemini-2.0-flash",
        description=(
            "Intelligent content strategy planner that analyzes user requests, "
            "identifies intent and topic, determines optimal content pipeline "
            "(social media, blog, or both), and orchestrates the appropriate agents "
            "for seamless content creation."
        ),
        input_schema=UserRequest,
        output_schema=PlannerOutput,
        output_key="planner_output",
        instruction=INSTRUCTION,
    )

    logger.info("Planner agent configured and ready for use")


except Exception as e:
    logger.error(f"Failed to initialize planner agent: {e}")
    raise
