"""
Content Writer Agent - Main orchestration agent for Lekhak AI

This is the primary agent that orchestrates the entire content creation pipeline.
It coordinates between:
1. Planner Agent - Analyzes requests and determines pipeline routing
2. Output Agent - Receives and outputs the planner's final analysis
"""

from ..utils.logger import get_logger

logger = get_logger("content_writer_agent")
logger.info("Initializing content writer agent")

try:
    from google.adk.agents import SequentialAgent
    from .planner_agent import planner_agent

    content_writer_agent = SequentialAgent(
        name="content_writer_agent",
        description="Orchestrates content creation by coordinating planning and output formatting.",
        sub_agents=[planner_agent],
    )

    logger.info("Content writer agent initialized with planner agent")
except Exception as e:
    logger.error(f"Failed to initialize content writer agent: {e}")
    raise
