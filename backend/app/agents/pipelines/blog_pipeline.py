from google.adk.agents import LlmAgent, SequentialAgent

from app.callbacks.agent_callbacks import (
    after_agent_callback,
    before_agent_callback,
    log_tool_error_callback,
)
from app.callbacks.model_callbacks import (
    log_model_request_callback,
    repair_json_callback,
)
from app.callbacks.tool_callbacks import (
    after_tool_callback,
    before_tool_callback,
)
from app.llm.providers import get_model
from app.prompts.blog_instruction.blog_optimizer_instruction import (
    blog_optimizer_instruction,
)
from app.prompts.blog_instruction.blog_research_instruction import (
    blog_research_instruction,
)
from app.prompts.blog_instruction.blog_writer_instruction import (
    blog_writer_instruction,
)
from app.schemas.blog_pipeline_schema import (
    BlogOptimizerOutput,
    BlogResearchOutput,
    BlogWriterOutput,
)
from app.tools.blog_tool import serp_google_search
from app.utils.loggers import get_logger

# Logger for the blog pipeline
logger_blog = get_logger("blog_pipeline")

blog_researcher = LlmAgent(
    name="blog_researcher",
    model=get_model(),
    description=(
        "Senior Content Strategist & Researcher. "
        "Responsible for conducting deep, multi-step research to find "
        "statistics, user personas, search intent, and competitor gaps. "
        "Uses SERP data to build a comprehensive foundation for high-quality blog content."
    ),
    instruction=blog_research_instruction,
    tools=[serp_google_search],
    output_schema=BlogResearchOutput,
    output_key="blog_research",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback],
    before_tool_callback=[before_tool_callback],
    after_tool_callback=[after_tool_callback],
    on_tool_error_callback=[log_tool_error_callback],
)

blog_writer = LlmAgent(
    name="blog_writer",
    model=get_model(),
    description="Transforms strategic research insights into a structured, SEO-optimized, and audience-focused blog post. Generates human-quality content that fills competitor gaps, incorporates verified data, and follows proven best practices for engagement and readability.",
    output_schema=BlogWriterOutput,
    instruction=blog_writer_instruction,
    output_key="blog_writer",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback],
)

blog_optimizer = LlmAgent(
    name="blog_optimizer",
    model=get_model(),
    description="Refines draft blog content into polished, human-sounding posts that are SEO-optimized, easy to read, and aligned with audience intent",
    instruction=blog_optimizer_instruction,
    output_schema=BlogOptimizerOutput,
    output_key="blog_optimizer",
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
    before_model_callback=[log_model_request_callback],
    after_model_callback=[repair_json_callback],
)



# The Blog Pipeline is a sequence of three specialized agents.
# 1. Researcher: Finds facts and statistics.
# 2. Writer: Drafts the content.
# 3. Optimizer: Polishes for SEO and readability.
blog_pipeline_agent = SequentialAgent(
    name="blog_pipeline",
    description="Professional blog creation suite: Research -> Write -> Optimize",
    sub_agents=[blog_researcher, blog_writer, blog_optimizer],
    before_agent_callback=[before_agent_callback],
    after_agent_callback=[after_agent_callback],
)

logger_blog.info("Blog pipeline initialized with professional guardrails and audit logs")
