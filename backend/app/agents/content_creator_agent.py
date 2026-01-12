from google.adk.agents import SequentialAgent

from app.agents.planner_agent import planner_agent
from app.agents.router_agent import RouterAgent
from app.callbacks.agent_callbacks import (
    after_agent_callback,
    before_agent_callback,
)
from app.utils.loggers import get_logger

# Logger for the master orchestrator
logger = get_logger("content_writer_agent")
logger.info("Initializing content writer agent")

try:
    # Create the RouterAgent instance to be used in the SequentialAgent
    router_agent_instance = RouterAgent()

    # The Content Creator Agent is the master entry point.
    # It first runs the Planner to understand the request,
    # then runs the Router to execute the specific content creation strategy.
    content_creator_agent = SequentialAgent(
        name="content_creator_agent",
        description="Master orchestration suite for Lekhak AI. Flow: Plan -> Route -> Execute",
        sub_agents=[planner_agent, router_agent_instance],
        
        # High-level audit logs for the entire session
        before_agent_callback=[before_agent_callback],
        after_agent_callback=[after_agent_callback],
    )
    logger.info("Master Content Creator initialized with full hierarchy audit logs")

except Exception as e:
    logger.error(f"Failed to initialize content writer agent: {e}")
    raise
