"""
OpenAI Provider - via LiteLlm Wrapper

Uses Google ADK's LiteLlm wrapper to integrate OpenAI models.

Requires:
    - OPENAI_API_KEY environment variable
    - litellm package installed

"""

from typing import Optional
from app.llm.providers.base import BaseLLMProvider
from app.llm.providers.litellm_patch import PatchedLiteLlm
from app.core.setting import OPENAI_API_KEY

class OpenAIProvider(BaseLLMProvider):
    """
    OpenAI Provider utilizing a patched LiteLlm wrapper to ensure 
    compatibility with Google ADK's structured output format.
    """
    
    def get_model(self, model: Optional[str] = None) -> PatchedLiteLlm:
        model_name = model or self.config.openai.default_model
            
        # Ensure model has the required LiteLlm 'openai/' prefix
        if not model_name.startswith("openai/"):
            model_name = f"openai/{model_name}"
            
        return PatchedLiteLlm(model=model_name, api_key=OPENAI_API_KEY)


def get_openai_model(model: Optional[str] = None) -> PatchedLiteLlm:
    """
    Utility function to retrieve an OpenAI model instance.
    Maintains backward compatibility for agent initialization.
    """
    provider = OpenAIProvider()
    return provider.get_model(model)


# Available OpenAI models for reference
OPENAI_MODELS = [
    "openai/gpt-4o",
    "openai/gpt-4o-mini",
    "openai/gpt-4-turbo",
    "openai/gpt-3.5-turbo",
]
