"""
Router Agent - Dynamic pipeline routing based on planner output
Clean, production-ready implementation following Google ADK best practices
"""

from typing import AsyncGenerator
from google.adk.agents import BaseAgent, ParallelAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types
from typing_extensions import override
from app.agents.pipelines.blog_pipeline import blog_pipeline_agent
from app.agents.pipelines.social_pipeline import social_pipeline_agent
from app.schemas.planner_schema import PlannerOutput
from app.utils.loggers import get_logger


logger = get_logger("router_agent")


class RouterAgent(BaseAgent):
    """
    Pure orchestrator agent that routes to appropriate content pipelines.
    Does not manipulate data - lets agents access what they need directly.
    """

    def __init__(self):
        super().__init__(
            name="router_agent",
            description="Intelligent routing agent that dynamically selects content pipelines.",
            sub_agents=[],  # Pure orchestrator
        )
        logger.info("Router agent initialized as pure orchestrator")

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Main routing logic - simple and clean"""

        try:
            # Step 1: Get planner output from session state
            planner_output_dict = ctx.session.state.get("planner_output")

            if not planner_output_dict:
                logger.error("No planner_output found in session state")
                yield self._error_event("Error: No planning data available for routing")
                return

            # Step 2: Validate and parse planner output
            planner_output = PlannerOutput.model_validate(planner_output_dict)
            logger.info(
                f"Routing decision: pipeline_type={planner_output.pipeline_type}"
            )

            # Step 3: Check if we should proceed
            if not planner_output.should_proceed:
                clarification = (
                    planner_output.clarification_needed
                    or "Unable to process request. Please provide more details."
                )
                logger.warning("Planner indicated should_proceed=False")
                yield self._text_event(clarification)
                return

            # Step 4: Route to appropriate pipeline
            pipeline_type = planner_output.pipeline_type.lower()

            if pipeline_type == "social":
                logger.info("→ Routing to SOCIAL pipeline")
                async for event in social_pipeline_agent.run_async(ctx):
                    yield event
                self._log_social_outputs(ctx)

            elif pipeline_type == "blog":
                logger.info("→ Routing to BLOG pipeline")
                async for event in blog_pipeline_agent.run_async(ctx):
                    yield event
                self._log_blog_outputs(ctx)

                blog_research_output = ctx.session.state.get("blog_research")
                if blog_research_output:
                    logger.info(f" Final Blog Research Output: {blog_research_output}")
                else:
                    logger.warning("No 'blog_research' found in context state")

            elif pipeline_type == "both":
                logger.info("→ Routing to BOTH pipelines (parallel)")
                async for event in self._execute_both_pipelines(ctx):
                    yield event

            elif pipeline_type == "none":
                clarification = (
                    planner_output.clarification_needed
                    or "I need more information to create content. Please clarify your request."
                )
                logger.warning("Pipeline type is NONE - requesting clarification")
                yield self._text_event(clarification)

            else:
                logger.error(f"Unknown pipeline type: {pipeline_type}")
                yield self._error_event(
                    f"Error: Unknown content type '{pipeline_type}'"
                )

        except Exception as e:
            logger.error(f"Router agent error: {e}", exc_info=True)
            yield self._error_event(f"An error occurred during routing: {str(e)}")

    async def _execute_both_pipelines(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """Execute social and blog pipelines in parallel"""

        logger.info("Executing both pipelines in parallel")

        try:
            parallel_executor = ParallelAgent(
                name="parallel_content_creator",
                description="Executes social and blog pipelines in parallel",
                sub_agents=[social_pipeline_agent, blog_pipeline_agent],
            )

            async for event in parallel_executor.run_async(ctx):
                yield event

            logger.info("Both pipelines completed successfully")
            self._log_social_outputs(ctx)
            self._log_blog_outputs(ctx)

        except Exception as e:
            logger.error(f"Parallel execution error: {e}", exc_info=True)
            yield self._error_event(f"Error during parallel execution: {str(e)}")

    def _log_social_outputs(self, ctx: InvocationContext) -> None:
        """Log social pipeline outputs for debugging"""
        try:
            social_research = ctx.session.state.get("social_research")
            social_content = ctx.session.state.get("social_content")
            optimized_content = ctx.session.state.get("optimized_social_content")

            logger.info(f"Social Research: {str(social_research)[:100]}")
            logger.info(f"Social Content: {str(social_content)[:100]}")
            logger.info(f"Optimized Content: {str(optimized_content)[:100]}")
        except Exception as e:
            logger.exception(f"Failed to log social outputs: {e}")

    def _log_blog_outputs(self, ctx: InvocationContext) -> None:
        """Log blog pipeline outputs for debugging"""
        try:
            blog_research = ctx.session.state.get("blog_research")
            blog_content = ctx.session.state.get("blog_content")

            logger.info(f"Blog Research: {str(blog_research)[:100]}")
            logger.info(f"Blog Content: {str(blog_content)[:100]}")
        except Exception as e:
            logger.exception(f"Failed to log blog outputs: {e}")

    def _text_event(self, text: str) -> Event:
        """Helper to create a text event"""
        return Event(
            author=self.name,
            content=types.Content(role="model", parts=[types.Part(text=text)]),
        )

    def _error_event(self, error_message: str) -> Event:
        """Helper to create an error event"""
        return Event(
            author=self.name,
            content=types.Content(role="model", parts=[types.Part(text=error_message)]),
        )
