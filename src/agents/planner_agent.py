from google.adk.agents import Agent
from src.schema.planner_schema import UserRequest, PlannerOutput

from src.utils.loggers import get_logger

from src.prompts.planner_instruction import INSTRUCTION

logger = get_logger("planner_agent")

planner_agent = Agent(
    name="planner_agent",
    model="gemini-2.0-flash",
    description="Planner Agent: decides content pipeline and extracts metadata",
    input_schema=UserRequest,
    output_schema=PlannerOutput,
    output_key="planner_output",
    instruction=INSTRUCTION,
)

logger.info("Planner agent initialized successfully")
