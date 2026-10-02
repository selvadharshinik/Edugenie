import logging
from backend.gemini_client import gemini_client
from backend.schemas.explanation import ExplainRequest, ExplainResponse
from backend.utils.prompts import EXPLANATION_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def explain_topic(request: ExplainRequest) -> ExplainResponse:
    """
    Generates a structured, simple explanation designed for learners.
    """
    prompt = EXPLANATION_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        topic=request.topic.strip()
    )

    explanation_text = gemini_client.generate_text(prompt, temperature=0.6)
    return ExplainResponse(
        topic=request.topic.strip(),
        explanation=explanation_text.strip()
    )
