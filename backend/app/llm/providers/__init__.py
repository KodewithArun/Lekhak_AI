from typing import Any, Optional
from app.core.llm_config import get_config
from app.llm.providers.gemini import get_gemini_model
from app.llm.providers.openai import get_openai_model

def get_model(model: Optional[str] = None) -> Any:
    """
    Factory function to get the configured LLM model based on active provider.
    """
    config = get_config()
    provider = config.active_provider.lower()
    
    if provider == "openai":
        return get_openai_model(model)
    else:
        # Default to Gemini
        return get_gemini_model(model)

__all__ = [
    "get_model",
    "get_gemini_model",
    "get_openai_model",
]
