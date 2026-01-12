import logging
from typing import Any, Optional

from google.adk.tools.base_tool import BaseTool
from google.adk.tools.tool_context import ToolContext

# Global logger for tool-related callbacks
logger = logging.getLogger("callbacks.tool")


async def before_tool_callback(
    tool: BaseTool, args: dict[str, Any], tool_context: ToolContext
) -> Optional[dict]:
    """
    Runs right before a tool (like Search) is executed.
    This provides visibility into what tools the AI is choosing to use.

    Args:
        tool: The tool being called
        args: Arguments being passed to the tool
        tool_context: Context for the tool execution

    Returns:
        Optional[dict]: Modified args or None to use original args
    """
    tool_name = getattr(tool, "name", type(tool).__name__)
    agent_name = getattr(tool_context, "agent_name", "unknown")
    logger.info(f"[Tool Call] Agent: {agent_name} | Tool: {tool_name}")
    return None  # Return None to proceed with original args


async def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict,
    **kwargs: Any,
) -> Optional[dict]:
    """
    Runs after a tool returns its data.
    Confirms that the tool has successfully provided information back to the agent.

    Args:
        tool: The tool that was called
        args: Arguments that were passed to the tool
        tool_context: Context for the tool execution
        tool_response: The response from the tool

    Returns:
        Optional[dict]: Modified response or None to use original response
    """
    tool_name = getattr(tool, "name", type(tool).__name__)
    agent_name = getattr(tool_context, "agent_name", "unknown")
    logger.debug(f"[Tool Response] Agent: {agent_name} | Tool: {tool_name} | Status: Received")
    return None  # Return None to proceed with original response
