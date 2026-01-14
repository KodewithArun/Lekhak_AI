"""
LLM Module - Provider-Based LLM Management

This module provides organized LLM provider integrations following Google ADK standards.
Each provider has its own module for clarity and easy switching.

Usage:
    # Import the provider you want to use
    from app.llm.providers.gemini import get_gemini_model
    from app.llm.providers.openai import get_openai_model
    
    # Use in your agent
    # agent = LlmAgent(model=get_gemini_model(), ...)
"""

# Export all provider functions for convenience
from app.llm.providers import (
    get_model,
    get_gemini_model,
    get_openai_model,
)

__all__ = [
    "get_model",
    "get_gemini_model",
    "get_openai_model",
]
