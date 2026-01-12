import json
import logging
from typing import Optional

# Global logger for JSON utilities
logger = logging.getLogger("json_utils")


def extract_json(text: str) -> str:
    """
    Robustly extracts the first valid JSON object or array from a string.

    This function identifies JSON boundaries by trying multiple start and end
    positions to bypass any conversational text (preambles or postambles) 
    that an LLM might include in its response.
    """
    if not text:
        return text

    # Find all potential starting brackets for JSON objects or arrays
    start_indices = [i for i, char in enumerate(text) if char in ("{", "[")]

    for start_idx in start_indices:
        # Determine the matching closing bracket
        end_char = "}" if text[start_idx] == "{" else "]"
        
        # Look for the last occurrence of the closing bracket to find the outermost block
        candidate_text = text[start_idx:]
        end_idx_relative = candidate_text.rfind(end_char)

        if end_idx_relative != -1:
            candidate = candidate_text[: end_idx_relative + 1]
            try:
                # Attempt to parse the candidate string as JSON to validate it
                json.loads(candidate)
                return candidate
            except json.JSONDecodeError:
                # If it's not valid JSON, we continue searching
                continue

    # If no valid JSON block is found, return the original text
    return text


def repair_json_if_needed(text: str) -> str:
    """
    A convenience wrapper that extracts JSON and logs when a repair was made.
    """
    if not text:
        return text

    extracted = extract_json(text)
    if extracted != text:
        logger.info("Raw LLM response was cleaned to extract valid JSON data.")
    return extracted
