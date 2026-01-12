from google.adk.agents import Agent

from app.callbacks.agent_callbacks import (
    after_agent_callback,
    before_agent_callback,
)
from app.callbacks.model_callbacks import (
    log_model_request_callback,
    repair_json_callback,
)
from app.llm.providers import get_model
from app.prompts.planner_instruction import INSTRUCTION
from app.schemas.planner_schema import PlannerOutput, UserRequest
from app.utils.loggers import get_logger

# Logger for the planner agent
logger = get_logger("planner_agent")


# The Planner Agent is the brain of the system.
# Its job is to take a user request, decide which content pipeline to trigger,
# and extract important metadata like topic, platform, and tone.
planner_agent = Agent(
    name="planner_agent",
    model=get_model(),
    description="Intelligent planner that orchestrates content strategy and metadata extraction",
    input_schema=UserRequest,
    output_schema=PlannerOutput,
    output_key="planner_output",
    instruction=INSTRUCTION,
    
    # Callback configuration for observability and data safety
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    
    # We use repair_json_callback to ensure that any conversational text added 
    # by the model doesn't break our strict Pydantic validation.
    after_model_callback=[repair_json_callback],
)


logger.info("Planner agent has been initialized with full audit and repair hooks")
