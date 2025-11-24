"""
Content Writer Agent - Main orchestration agent for Lekhak AI

This is the primary agent that orchestrates the entire content creation pipeline.
It coordinates between:
1. Planner Agent - Analyzes requests and determines pipeline routing
2. Pipeline Agent - Manages the execution of content generation tasks
"""

from google.adk.agents import SequentialAgent

from src.agents.planner_agent import planner_agent
from src.utils.loggers import get_logger

logger = get_logger("content_writer_agent")
logger.info("Initializing content writer agent")

try:
    content_creator_agent = SequentialAgent(
        name="content_creator_agent",
        description="Orchestrates content writer by coordinating planning and pipeline execution.",
        sub_agents=[planner_agent],
    )
    logger.info("Content writer agent initialized with planner agent")
except Exception as e:
    logger.error(f"Failed to initialize content writer agent: {e}")
    raise
