from google.adk.agents import Agent
from src.schema.planner_schema import UserRequest, PlannerOutput

from src.utils.loggers import get_logger

from src.prompts.planner_instruction import INSTRUCTION
from src.utils.config import GEMINI_MODEL

logger = get_logger("planner_agent")

planner_agent = Agent(
    name="planner_agent",
    model=GEMINI_MODEL,
    description="Planner Agent: decides content pipeline and extracts metadata",
    input_schema=UserRequest,
    output_schema=PlannerOutput,
    output_key="planner_output",
    instruction=INSTRUCTION,
)

logger.info("Planner agent initialized successfully")
