"""
Router Agent - Dynamic pipeline routing based on planner output
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
    Custom routing agent that dynamically selects and executes pipelines
    based on PlannerOutput. This agent is a pure orchestrator.
    """

    def __init__(self):

        # The sub_agents list is now EMPTY.
        # This agent orchestrates other agents but does not formally parent them.
        sub_agents_list = []

        super().__init__(
            name="router_agent",
            description="Intelligent routing agent that dynamically selects content pipelines.",
            # adding sub_agents as empty list
            sub_agents=sub_agents_list,
        )
        logger.info("Router agent initialized as a pure orchestrator.")

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        try:
            planner_output_dict = ctx.session.state.get("planner_output")

            if not planner_output_dict:
                logger.error("No planner_output found in context")
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part(
                                text="Error: No planning data available for routing"
                            )
                        ],
                    ),
                )
                return

            planner_output = PlannerOutput.model_validate(planner_output_dict)
            logger.info(
                f"Routing decision: pipeline_type={planner_output.pipeline_type}"
            )

            if not planner_output.should_proceed:
                clarification = (
                    planner_output.clarification_needed
                    or "Unable to process request. Please provide more details."
                )
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model", parts=[types.Part(text=clarification)]
                    ),
                )
                return

            pipeline_type = planner_output.pipeline_type.lower()

            if pipeline_type == "social":
                logger.info("Routing to SOCIAL pipeline")

                # Call the global singleton instance directly
                async for event in social_pipeline_agent.run_async(ctx):
                    yield event

            elif pipeline_type == "blog":
                logger.info("Routing to BLOG pipeline")

                # Call the global singleton instance directly
                async for event in blog_pipeline_agent.run_async(ctx):
                    yield event

                blog_research_output = ctx.session.state.get("blog_research")
                if blog_research_output:
                    logger.info(f" Final Blog Research Output: {blog_research_output}")
                else:
                    logger.warning("No 'blog_research' found in context state")

            elif pipeline_type == "both":
                logger.info("Routing to BOTH pipelines (parallel)")
                async for event in self._execute_both_pipelines(ctx):
                    yield event

            elif pipeline_type == "none":
                clarification = (
                    planner_output.clarification_needed
                    or "I need more information to create content. Please clarify your request."
                )
                logger.warning("Pipeline type is NONE")
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model", parts=[types.Part(text=clarification)]
                    ),
                )
            else:
                logger.error(f"Unknown pipeline type: {pipeline_type}")
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role="model",
                        parts=[
                            types.Part(
                                text=f"Error: Unknown content type '{pipeline_type}'"
                            )
                        ],
                    ),
                )

        except Exception as e:
            logger.error(f"Router agent error: {e}", exc_info=True)
            yield Event(
                author=self.name,
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(text=f"An error occurred during routing: {str(e)}")
                    ],
                ),
            )

    # We call the agents directly in _run_async_impl.

    async def _execute_both_pipelines(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        logger.info("Executing both pipelines in parallel")
        try:
            # This is the ONLY place where the pipelines are given a temporary parent.
            parallel_executor = ParallelAgent(
                name="parallel_content_creator",
                description="Executes social and blog pipelines in parallel",
                # Pass the global singleton instances here
                sub_agents=[social_pipeline_agent, blog_pipeline_agent],
            )

            async for event in parallel_executor.run_async(ctx):
                yield event

            logger.info("Both pipelines completed successfully")

        except Exception as e:
            logger.error(f"Parallel execution error: {e}", exc_info=True)
            yield Event(
                author=self.name,
                content=types.Content(
                    role="model",
                    parts=[
                        types.Part(text=f"Error during parallel execution: {str(e)}")
                    ],
                ),
            )
