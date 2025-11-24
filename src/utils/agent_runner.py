# src/utils/agent_runner.py
"""Agent Runner Utilities for Lekhak AI"""

from google.adk.runners import Runner
from google.genai.types import Content, Part
from src.utils.loggers import get_logger

logger = get_logger("agent_runner")


async def call_agent_async(
    runner: Runner, user_id: str, session_id: str, user_input: str
):
    """
    Call the agent asynchronously with user input and display the response.

    Args:
        runner: The ADK Runner instance
        user_id: User identifier
        session_id: Session identifier
        user_input: User's message/query
    """
    try:
        logger.info(f"Processing user input: {user_input[:50]}...")

        # Build a Content object with role='user' (required by ADK)
        user_content = Content(
            role="user",
            parts=[Part(text=user_input)],
        )

        # Run the agent  may return an async generator
        response_iter = runner.run_async(
            user_id=user_id,
            session_id=session_id,
            new_message=user_content,
        )

        # Collect the final content (handle async generator or single response)
        final_content = None
        if hasattr(response_iter, "__aiter__"):
            async for part in response_iter:
                if hasattr(part, "content"):
                    final_content = part.content
        else:
            if hasattr(response_iter, "content"):
                final_content = response_iter.content

        if final_content:
            print(f"\nAgent: {final_content}\n")
            logger.info("Agent response delivered successfully")
        else:
            print(
                "\nAgent: I processed your request but have no response to display.\n"
            )
            logger.warning("Agent returned no content")

    except Exception as e:
        error_msg = f"Error processing request: {str(e)}"
        print(f"\nAgent: {error_msg}\n")
        logger.error(error_msg, exc_info=True)
