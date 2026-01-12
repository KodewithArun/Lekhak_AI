import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from app.utils.json_utils import extract_json

# Global logger for model-related callbacks
logger = logging.getLogger("callbacks.model")


async def log_model_request_callback(
    callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """
    Logs details about the outgoing request to the LLM.
    Helps developers track which model is being used by which agent.

    Args:
        callback_context: The callback context containing agent information
        llm_request: The request being sent to the LLM

    Returns:
        Optional[LlmResponse]: A response to use instead of calling the LLM, or None to proceed
    """
    model_name = getattr(llm_request, "model", "unknown")
    logger.debug(f"[Model Request] Agent: {callback_context.agent_name} | Model: {model_name}")
    return None  # Return None to proceed with the actual LLM call


async def repair_json_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Production-grade fix for validation errors.
    LLMs sometimes include conversational text alongside JSON data. This function
    extracts the raw JSON so that the system doesn't crash during validation.

    Args:
        callback_context: The callback context containing agent information
        llm_response: The response from the LLM

    Returns:
        Optional[LlmResponse]: Modified response or None to use original
    """
    if llm_response.content and llm_response.content.parts:
        for part in llm_response.content.parts:
            if hasattr(part, "text") and part.text:
                original_text = part.text
                cleaned_text = extract_json(original_text)

                if cleaned_text != original_text:
                    logger.info(
                        f"[JSON Repair] Successfully cleaned response for agent: {callback_context.agent_name}"
                    )
                    part.text = cleaned_text
    return None  # Return None to use the (potentially modified) response

