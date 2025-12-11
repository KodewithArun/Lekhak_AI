"""
Content Writer Agent - Main orchestration agent for Lekhak AI
"""

from google.adk.agents import SequentialAgent
from app.agents.planner_agent import planner_agent
from app.agents.router_agent import RouterAgent
from app.utils.loggers import get_logger

logger = get_logger("content_writer_agent")
logger.info("Initializing content writer agent")

try:
    # Create the RouterAgent instance to be used in the SequentialAgent
    router_agent_instance = RouterAgent()

    # Create the main SequentialAgent using the instance
    content_creator_agent = SequentialAgent(
        name="content_creator_agent",
        description="Master orchestrator for Lekhak AI content creation. Flow: 1. Planner Agent 2. Router Agent",
        sub_agents=[planner_agent, router_agent_instance],
    )
    logger.info("Content writer agent initialized successfully")

except Exception as e:
    logger.error(f"Failed to initialize content writer agent: {e}")
    raise
