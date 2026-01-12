"""
Gemini Provider - Google ADK Native

Gemini models are natively supported by Google ADK, so we just return
the model string directly.

"""

from typing import Optional
import os
from app.llm.providers.base import BaseLLMProvider
from app.core.setting import GOOGLE_API_KEY

class GeminiProvider(BaseLLMProvider):
    """
    Google Gemini Provider.
    Returns the model string directly as Google ADK supports Gemini natively.
    """
    
    def get_model(self, model: Optional[str] = None) -> str:
        # Ensure API key is set in environment for ADK native client
        if GOOGLE_API_KEY and "GOOGLE_API_KEY" not in os.environ:
            os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY
            
        if model:
            return model
        return self.config.gemini.default_model

def get_gemini_model(model: Optional[str] = None) -> str:
    """
    Wrapper for backward compatibility.
    Get a Gemini model string for use with ADK agents.
    """
    provider = GeminiProvider()
    return provider.get_model(model)


# Available Gemini models for reference
GEMINI_MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro", 
    "gemini-1.5-flash",
    "gemini-1.5-pro",
]
