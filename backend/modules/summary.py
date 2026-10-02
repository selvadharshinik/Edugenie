import logging
from backend.gemini_client import gemini_client
from backend.schemas.summary import SummarizeRequest, SummarizeResponse
from backend.utils.prompts import SUMMARY_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def summarize_text(request: SummarizeRequest) -> SummarizeResponse:
    """
    Generates a concise educational summary suitable for revision.
    """
    prompt = SUMMARY_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        text=request.text.strip()
    )

    summary_output = gemini_client.generate_text(prompt, temperature=0.5)
    return SummarizeResponse(summary=summary_output.strip())
