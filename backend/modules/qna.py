import logging
from backend.gemini_client import gemini_client
from backend.schemas.qa import QARequest, QAResponse
from backend.utils.prompts import QA_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def answer_question(request: QARequest) -> QAResponse:
    """
    Answers educational questions clearly and concisely.
    """
    prompt = QA_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        question=request.question.strip()
    )

    answer_text = gemini_client.generate_text(prompt, temperature=0.5)
    return QAResponse(answer=answer_text.strip())
