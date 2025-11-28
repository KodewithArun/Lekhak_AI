"""
Content Writer Agent - Main orchestration agent for Lekhak AI
"""

from google.adk.agents import SequentialAgent
from src.agents.planner_agent import planner_agent
from src.agents.pipelines.social_pipeline import social_pipeline_agent
from src.agents.pipelines.blog_pipeline import blog_pipeline_agent
from src.agents.router_agent import RouterAgent
from src.utils.loggers import get_logger

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
