import logging
from typing import Optional

from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

from app.utils.json_utils import extract_json
from app.utils.loggers import get_logger

# Global logger for model-related callbacks - uses custom file logger
logger = get_logger("callbacks.model")


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



async def log_token_usage_callback(
    callback_context: CallbackContext, llm_response: LlmResponse
) -> Optional[LlmResponse]:
    """
    Tracks and logs token usage for cost monitoring.
    Works with both Google Gemini (native) and OpenAI (via wrapper).
    """
    try:
        input_tokens = 0
        output_tokens = 0
        
        # 1. Try generic dictionary access (OpenAI/LiteLLM usually has this)
        usage_dict = getattr(llm_response, "usage", None)
        
        # 2. Try Google Native format (usage_metadata)
        usage_metadata = getattr(llm_response, "usage_metadata", None)

        if usage_metadata:
            # Google GenerativeAI format (handling both object and dict)
            if isinstance(usage_metadata, dict):
                input_tokens = usage_metadata.get("prompt_token_count", 0) or usage_metadata.get("prompt_tokens", 0)
                output_tokens = usage_metadata.get("candidates_token_count", 0) or usage_metadata.get("completion_tokens", 0)
            else:
                # Try snake_case (standard)
                input_tokens = getattr(usage_metadata, "prompt_token_count", 0)
                output_tokens = getattr(usage_metadata, "candidates_token_count", 0)
                
                # Try camelCase (some versions) if zero
                if input_tokens == 0:
                     input_tokens = getattr(usage_metadata, "promptTokenCount", 0)
                if output_tokens == 0:
                     output_tokens = getattr(usage_metadata, "candidatesTokenCount", 0)

        elif usage_dict:
            # OpenAI / LiteLLM format
            if isinstance(usage_dict, dict):
                input_tokens = usage_dict.get("prompt_tokens", 0)
                output_tokens = usage_dict.get("completion_tokens", 0)
            else:
                input_tokens = getattr(usage_dict, "prompt_tokens", 0)
                output_tokens = getattr(usage_dict, "completion_tokens", 0)
        
        total_tokens = input_tokens + output_tokens
        
        if total_tokens > 0:
            logger.info(
                f"[Token Usage] Agent: {callback_context.agent_name} | "
                f"Input: {input_tokens} | Output: {output_tokens} | Total: {total_tokens}"
            )
        else:
            # Debug log to help find why it's missing (only on warning level to avoid spam)
            logger.warning(
                f"[Token Usage Missing] Agent: {callback_context.agent_name}. "
                f"Has usage_metadata: {bool(usage_metadata)}, Has usage: {bool(usage_dict)}"
            )
            
    except Exception as e:
        logger.error(f"Failed to track token usage: {e}")
        
    return None


