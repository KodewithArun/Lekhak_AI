"""
Lekhak AI - AI-Powered Content Creation Platform
Main entry point for the ADK web interface
"""

from src.agents.content_creator_agent import content_creator_agent
from src.utils.loggers import get_logger

logger = get_logger("main")
logger.info("Initializing Lekhak AI root agent")

try:

    # Export the root agent for ADK
    root_agent = content_creator_agent

    logger.info("Lekhak AI root agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Lekhak AI root agent: {e}")
    raise
