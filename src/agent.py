"""
Lekhak AI - AI-Powered Content Creation Platform
Main entry point for the ADK web interface
"""

from .utils.logger import get_logger

logger = get_logger("main")
logger.info("Initializing Lekhak AI root agent")

try:
    from .agents import content_writer_agent

    # Export the root agent for ADK
    root_agent = content_writer_agent

    logger.info("Lekhak AI root agent initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Lekhak AI root agent: {e}")
    raise
