import logging
from typing import Any, AsyncGenerator, Dict, Optional

from google.adk.models.lite_llm import LiteLlm
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse

# Logger for the LiteLLM adaptation layer
logger = logging.getLogger("litellm_patch")


class PatchedLiteLlm(LiteLlm):
    """
    A professional adaptation layer for LiteLlm.
    
    This class fixes a compatibility issue where Google ADK uses 'response_schema' 
    but OpenAI's API strictly requires 'json_schema'. This allows the project 
    to switch between model providers seamlessly.
    """

    async def generate_content_async(
        self, llm_request: LlmRequest, stream: bool = False
    ) -> AsyncGenerator[LlmResponse, None]:
        """
        Intercepts the generation process to fix model-specific parameters 
        before they are sent to the provider.
        """

        original_acompletion = self.llm_client.acompletion

        async def patched_acompletion(**kwargs):
            # Special handling for OpenAI models to ensure structured output works correctly
            if self.model.startswith("openai/"):
                if "response_format" in kwargs and isinstance(
                    kwargs["response_format"], dict
                ):
                    rf = kwargs["response_format"]
                    if "response_schema" in rf:
                        schema = rf.pop("response_schema")
                        
                        # Translate 'response_schema' to OpenAI's 'json_schema' format
                        rf["type"] = "json_schema"
                        rf["json_schema"] = {
                            "name": "structured_output",
                            "strict": True,
                            "schema": schema,
                        }
                        logger.info(
                            f"Applied OpenAI parameter conversion for model: {self.model}"
                        )

            return await original_acompletion(**kwargs)

        # Temporary patch of the completion method for this specific call
        self.llm_client.acompletion = patched_acompletion
        try:
            async for response in super().generate_content_async(llm_request, stream):
                yield response
        finally:
            # Restore the original method immediately after the call
            self.llm_client.acompletion = original_acompletion

