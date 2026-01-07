"""
JSON Repair Utility for LLM Outputs

Production-ready sanitization for malformed LLM JSON.
Handles common issues:
- Text preamble before JSON
- Markdown code block wrappers
- Invalid escape sequences
- Trailing commas
"""

import re
import json
import logging
from typing import Optional, Tuple

logger = logging.getLogger("json_repair")


def extract_json_from_text(text: str) -> str:
    """
    Extract JSON object from text that may contain preamble or suffix.
    Finds the outermost { } pair and extracts it.
    """
    if not text:
        return text

    text = text.strip()

    # If already starts with {, just return
    if text.startswith("{"):
        # Find matching closing brace
        brace_count = 0
        end_idx = -1
        for i, char in enumerate(text):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    end_idx = i
                    break
        if end_idx != -1:
            return text[: end_idx + 1]
        return text

    # Find first { and extract from there
    first_brace = text.find("{")
    if first_brace == -1:
        return text  # No JSON found

    # Extract from first { to matching }
    brace_count = 0
    end_idx = -1
    for i in range(first_brace, len(text)):
        char = text[i]
        if char == "{":
            brace_count += 1
        elif char == "}":
            brace_count -= 1
            if brace_count == 0:
                end_idx = i
                break

    if end_idx != -1:
        extracted = text[first_brace : end_idx + 1]
        if first_brace > 0:
            logger.info(
                f"Extracted JSON from text (removed {first_brace} chars of preamble)"
            )
        return extracted

    # Fallback: return from first brace to end
    return text[first_brace:]


def strip_markdown_blocks(text: str) -> str:
    """
    Remove markdown code block wrappers from LLM output.
    Handles: ```json ... ```, ``` ... ```, and variations.
    """
    if not text:
        return text

    text = text.strip()

    # Pattern: ```json\n...\n``` or ```\n...\n```
    pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.match(pattern, text, re.DOTALL | re.IGNORECASE)

    if match:
        return match.group(1).strip()

    # Also handle inline code blocks
    if text.startswith("```") and text.endswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```$", "", text)
        return text.strip()

    return text


def fix_escape_sequences(text: str) -> str:
    """
    Fix invalid escape sequences in JSON strings.
    LLMs often produce unescaped newlines/tabs inside string values.
    """
    if not text:
        return text

    result = []
    in_string = False
    i = 0

    while i < len(text):
        char = text[i]

        if char == '"' and (i == 0 or text[i - 1] != "\\"):
            in_string = not in_string
            result.append(char)
        elif in_string and char == "\\" and i + 1 < len(text):
            next_char = text[i + 1]
            valid_escapes = {'"', "\\", "/", "b", "f", "n", "r", "t", "u"}
            if next_char in valid_escapes:
                result.append(char)
            else:
                result.append("\\\\")
        elif in_string and char == "\n":
            result.append("\\n")
            i += 1
            continue
        elif in_string and char == "\r":
            result.append("\\r")
            i += 1
            continue
        elif in_string and char == "\t":
            result.append("\\t")
            i += 1
            continue
        else:
            result.append(char)

        i += 1

    return "".join(result)


def fix_trailing_commas(text: str) -> str:
    """
    Remove trailing commas before closing brackets/braces.
    Common LLM mistake: {"key": "value",}
    """
    if not text:
        return text

    text = re.sub(r",\s*}", "}", text)
    text = re.sub(r",\s*]", "]", text)

    return text


def balance_json_brackets_and_quotes(text: str) -> str:
    """
    Attempt to balance unclosed brackets and quotes if the JSON is truncated.
    """
    if not text:
        return text

    # Check for unclosed string
    open_quotes = text.count('"') - text.count('\\"')
    if open_quotes % 2 != 0:
        text += '"'

    stack = []
    for char in text:
        if char == '{':
            stack.append('}')
        elif char == '[':
            stack.append(']')
        elif char == '}' or char == ']':
            if stack:
                if stack[-1] == char:
                    stack.pop()

    # Append missing closing brackets in reverse order
    while stack:
        text += stack.pop()

    return text


def repair_json(text: str) -> Tuple[str, bool]:
    """
    Full JSON repair pipeline.

    Returns:
        Tuple[str, bool]: (repaired_text, was_modified)
    """
    if not text:
        return text, False

    original = text

    # Step 1: Strip markdown blocks
    text = strip_markdown_blocks(text)

    # Step 2: Extract JSON from mixed text (handles preamble)
    text = extract_json_from_text(text)

    # Step 3: Fix escape sequences
    text = fix_escape_sequences(text)

    # Step 4: Fix trailing commas
    text = fix_trailing_commas(text)

    # Step 5: Balance truncated JSON
    text = balance_json_brackets_and_quotes(text)

    # Step 6: Verify it's valid JSON
    try:
        json.loads(text)
        was_modified = text != original
        if was_modified:
            logger.info("JSON repaired successfully")
        return text, was_modified
    except json.JSONDecodeError as e:
        logger.warning(f"JSON repair incomplete, still has errors: {e}")
        return text, True


def validate_and_repair(text: str, schema_name: str = "unknown") -> Optional[str]:
    """
    Validate JSON and attempt repair if invalid.
    """
    if not text:
        logger.error(f"Empty input for {schema_name}")
        return None

    # First, try as-is
    try:
        json.loads(text)
        return text
    except json.JSONDecodeError:
        pass

    # Attempt repair
    repaired, was_modified = repair_json(text)

    try:
        json.loads(repaired)
        if was_modified:
            logger.info(f"Successfully repaired JSON for {schema_name}")
        return repaired
    except json.JSONDecodeError as e:
        logger.error(f"JSON repair failed for {schema_name}: {e}")
        return None
