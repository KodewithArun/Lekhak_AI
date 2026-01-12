import logging
from typing import Any, Dict, Optional

from google.adk.agents.callback_context import CallbackContext
from google.genai import types

# Global logger for agent-related callbacks
logger = logging.getLogger("callbacks.agent")


async def before_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Hook that runs immediately before an agent starts its work.
    We use this to log the beginning of a task for better debugging.

    Args:
        callback_context: The callback context containing agent information

    Returns:
        Optional[types.Content]: Content to use instead of running the agent, or None to proceed
    """
    logger.info(
        f"[Agent Start] Name: {callback_context.agent_name} | "
        f"Invocation ID: {callback_context.invocation_id}"
    )
    return None  # Return None to let the agent proceed normally


async def after_agent_callback(
    callback_context: CallbackContext,
) -> Optional[types.Content]:
    """
    Hook that runs after an agent successfully finishes its work.
    Confirms the agent has completed its designated task.

    Args:
        callback_context: The callback context containing agent information

    Returns:
        Optional[types.Content]: Modified content or None to use original
    """
    logger.info(f"[Agent Complete] Name: {callback_context.agent_name} | Status: Success")
    return None  # Return None to use the original response


async def log_tool_error_callback(
    tool: Any, args: Dict[str, Any], context: Any, error: Exception
) -> Optional[Dict]:
    """
    Special hook that captures errors during tool execution (like API failures).
    This ensures that tool-level issues are recorded professionally in our logs.
    """
    tool_name = getattr(tool, "name", "unknown_tool")
    logger.error(f"[Tool Error] Tool: {tool_name} | Args: {args} | Error: {str(error)}")
    
    # Returning None tells the system to continue with default error handling
    return None
