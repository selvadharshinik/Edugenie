import json
import re
import logging
from typing import Any, Union, Dict, List

logger = logging.getLogger(__name__)

def parse_json_from_llm(raw_text: str) -> Union[Dict[str, Any], List[Any]]:
    """
    Extracts and parses JSON from raw LLM text responses.
    Handles:
    - Markdown code blocks (```json ... ``` or ``` ...)
    - Trailing commas or stray backticks
    - Direct JSON strings
    """
    if not raw_text or not raw_text.strip():
        raise ValueError("Empty response received from LLM model.")

    cleaned = raw_text.strip()

    # Remove markdown code fences if present
    code_fence_pattern = r"^```(?:json)?\s*\n?(.*?)\n?```$"
    match = re.search(code_fence_pattern, cleaned, re.DOTALL | re.IGNORECASE)
    if match:
        cleaned = match.group(1).strip()
    else:
        # Fallback: find first '[' or '{' and last ']' or '}'
        first_bracket = min(
            [pos for pos in [cleaned.find('['), cleaned.find('{')] if pos != -1],
            default=-1
        )
        last_bracket = max(
            [cleaned.rfind(']'), cleaned.rfind('}')]
        )
        if first_bracket != -1 and last_bracket != -1 and last_bracket > first_bracket:
            cleaned = cleaned[first_bracket:last_bracket + 1]

    # Attempt to parse
    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as err:
        logger.warning(f"Initial JSON parse failed: {err}. Attempting secondary cleanup.")
        # Trailing comma cleanup
        cleaned_secondary = re.sub(r',\s*([}\]])', r'\1', cleaned)
        try:
            return json.loads(cleaned_secondary)
        except json.JSONDecodeError as err2:
            logger.error(f"Failed to parse JSON from LLM: {err2}\nRaw text:\n{raw_text}")
            raise ValueError(f"Could not parse valid JSON from AI output: {str(err2)}")
