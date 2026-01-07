"""
ADK Callbacks for JSON Repair
"""

import json
import logging
from typing import Optional

from google.adk.models import LlmResponse
from google.genai import types

from app.utils.json_repair import repair_json
from app.utils.loggers import get_logger

logger = get_logger("json_callbacks")


def repair_json_after_model(
    callback_context,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    if not llm_response:
        return None
    
    try:
        content = llm_response.content
        if not content or not content.parts:
            return None
        
        # Extract text
        original_text = ""
        for part in content.parts:
            if hasattr(part, 'text') and part.text:
                original_text += part.text
        
        if not original_text:
            return None
            
        stripped = original_text.strip()
        
        # Check if this contains JSON (look for curly braces)
        if '{' not in stripped:
            return None
        
        # Apply repair
        repaired_text, was_modified = repair_json(original_text)
        
        if was_modified:
            agent_name = getattr(callback_context, 'agent_name', 'unknown')
            logger.info(f"[{agent_name}] JSON repaired via callback")
            
            # Create new content with repaired text
            new_part = types.Part(text=repaired_text)
            new_content = types.Content(
                role=content.role if hasattr(content, 'role') else "model",
                parts=[new_part]
            )
            
            return LlmResponse(
                content=new_content,
                partial=getattr(llm_response, 'partial', False),
                turn_complete=getattr(llm_response, 'turn_complete', True),
            )
        
        return None
        
    except Exception as e:
        logger.error(f"Error in repair_json_after_model: {e}", exc_info=True)
        return None
