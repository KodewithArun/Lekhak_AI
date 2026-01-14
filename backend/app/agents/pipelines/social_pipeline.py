from google.adk.agents import LlmAgent, SequentialAgent

from app.callbacks.agent_callbacks import (
    after_agent_callback,
    before_agent_callback,
    log_tool_error_callback,
)
from app.callbacks.model_callbacks import (
    log_model_request_callback,
    repair_json_callback,
    log_token_usage_callback,
)
from app.callbacks.tool_callbacks import (
    after_tool_callback,
    before_tool_callback,
)
from app.llm.providers import get_model
from app.prompts.social_instructions.optimizer_instruction import (
    OPTIMIZER_AGENT_INSTRUCTION,
)
from app.prompts.social_instructions.research_instruction import (
    RESEARCH_AGENT_INSTRUCTION,
)
from app.prompts.social_instructions.writer_instruction import (
    SOCIAL_AGENT_INSTRUCTION,
)
from app.schemas.social_pipeline_schema import (
    OptimizedContent,
    SocialContentOutput,
    SocialResearchOutput,
)
from app.tools.social_search_tool import serp_platform_search
from app.utils.loggers import get_logger

# Logger for the social media pipeline
logger = get_logger("social_pipeline")


social_researcher = LlmAgent(
    name="social_researcher",
    model=get_model(),
    description="Conducts in-depth research on social media trends, audience preferences, and competitor content for various platforms to inform content creation.",
    instruction=RESEARCH_AGENT_INSTRUCTION,
    tools=[serp_platform_search],
    output_schema=SocialResearchOutput,
    output_key="social_research",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback, log_token_usage_callback],
    before_tool_callback=[before_tool_callback],
    after_tool_callback=[after_tool_callback],
    on_tool_error_callback=[log_tool_error_callback],
)


social_writer = LlmAgent(
    name="social_writer",
    model=get_model(),
    description="Generates high-quality social media content including captions, main content, hashtags, hooks, and optional CTAs based on research insights for each platform.",
    instruction=SOCIAL_AGENT_INSTRUCTION,
    output_schema=SocialContentOutput,
    output_key="social_content",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback, log_token_usage_callback],
)


social_optimizer = LlmAgent(
    name="social_optimizer",
    model=get_model(),
    description="Takes AI-generated social media content and optimizes it to be human-like, engaging, and platform-ready with trending hashtags, captions, and optional hooks/CTAs based on platform conventions.",
    instruction=OPTIMIZER_AGENT_INSTRUCTION,
    output_schema=OptimizedContent,
    output_key="optimized_social_content",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback, log_token_usage_callback],
)



# The Social Pipeline is a sequence of three specialized agents.
# 1. Researcher: Tracks trends and competitor strategies.
# 2. Writer: Creates platform-specific drafts.
# 3. Optimizer: Finalizes hashtags, hooks, and CTAs.
social_pipeline_agent = SequentialAgent(
    name="social_pipeline",
    description="Platform-ready social media creation suite: Research -> Write -> Optimize",
    sub_agents=[social_researcher, social_writer, social_optimizer],
    
    # Audit hooks for the entire pipeline duration
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
)

logger.info("Social pipeline initialized with professional guardrails and audit logs")
