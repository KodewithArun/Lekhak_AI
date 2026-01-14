from typing import Optional
from pydantic import BaseModel, Field
from app.core.setting import GEMINI_MODEL, OPENAI_MODEL, ACTIVE_PROVIDER

class GeminiConfig(BaseModel):
    default_model: str = Field(default=GEMINI_MODEL, description="Default Gemini model to use")

class OpenAIConfig(BaseModel):
    default_model: str = Field(default=OPENAI_MODEL, description="Default OpenAI model to use")

class LLMConfig(BaseModel):
    active_provider: str = Field(default="gemini", description="Active LLM provider (gemini, openai)")
    gemini: GeminiConfig = Field(default_factory=GeminiConfig)
    openai: OpenAIConfig = Field(default_factory=OpenAIConfig)

_config_instance: Optional[LLMConfig] = None

def load_config() -> LLMConfig:
    """
    Load configuration from environment variables.
    Returns the singleton config instance.
    """
    global _config_instance
    
    if _config_instance:
        return _config_instance
        
    # Create config instance populated by environment variable defaults in Pydantic models
    _config_instance = LLMConfig()
    
    # Explicitly override active_provider from environment if provided (extra safety)
    if ACTIVE_PROVIDER:
        _config_instance.active_provider = ACTIVE_PROVIDER
        
    return _config_instance

def get_config() -> LLMConfig:
    """Get the global configuration instance."""
    return load_config()
