from abc import ABC, abstractmethod
from typing import Any, Optional
from app.core.llm_config import get_config, LLMConfig

class BaseLLMProvider(ABC):
    """
    Abstract base class for all LLM providers.
    Ensures a consistent interface for configuration and model retrieval.
    """
    
    def __init__(self):
        self.config: LLMConfig = get_config()

    @abstractmethod
    def get_model(self, model: Optional[str] = None) -> Any:
        """
        Get the configured LLM model.
        
        Args:
            model: Optional model name to override the default.
            
        Returns:
            The model instance (str for Gemini, LiteLlm for others)
        """
        pass
