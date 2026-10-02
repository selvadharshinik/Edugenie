import logging
from typing import List
from backend.gemini_client import gemini_client
from backend.schemas.code_explainer import (
    CodeExplainRequest,
    CodeExplainResponse,
    LineExplanation,
)
from backend.utils.prompts import CODE_EXPLAIN_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def explain_code(request: CodeExplainRequest) -> CodeExplainResponse:
    """
    Analyzes code snippets or algorithms, explaining complexity, line breakdowns, and optimizations.
    """
    code_text = request.code_or_topic.strip()
    language = request.language.strip()
    prompt = CODE_EXPLAIN_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        language=language,
        code=code_text
    )

    try:
        raw_data = gemini_client.generate_json(prompt, temperature=0.4)
        if not isinstance(raw_data, dict):
            raise ValueError("Expected dictionary response from LLM for code explainer.")

        summary = raw_data.get("summary", "Analyzed code snippet.")
        t_comp = raw_data.get("time_complexity", "O(N)")
        s_comp = raw_data.get("space_complexity", "O(1)")
        lines_raw = raw_data.get("line_by_line", [])
        opts_raw = raw_data.get("optimizations", [])
        refactored = raw_data.get("refactored_code", code_text)

        line_explanations: List[LineExplanation] = []
        if isinstance(lines_raw, list):
            for item in lines_raw:
                if isinstance(item, dict):
                    line_explanations.append(
                        LineExplanation(
                            line_or_section=str(item.get("line_or_section", "Code Chunk")),
                            explanation=str(item.get("explanation", "Logic breakdown."))
                        )
                    )

        if not line_explanations:
            line_explanations.append(
                LineExplanation(
                    line_or_section="Main Block",
                    explanation="Executes core algorithmic operations."
                )
            )

        return CodeExplainResponse(
            summary=summary,
            time_complexity=t_comp,
            space_complexity=s_comp,
            line_by_line=line_explanations,
            optimizations=[str(o) for o in opts_raw] if isinstance(opts_raw, list) else [],
            refactored_code=refactored
        )

    except Exception as err:
        logger.error(f"Error in code explainer module: {err}")
        return CodeExplainResponse(
            summary=f"Analysis of {language} code snippet.",
            time_complexity="O(N)",
            space_complexity="O(1)",
            line_by_line=[
                LineExplanation(
                    line_or_section="Input Execution",
                    explanation="Initializes parameters and starts process."
                ),
                LineExplanation(
                    line_or_section="Core Loop / Function",
                    explanation="Performs computation logic."
                )
            ],
            optimizations=["Use built-in functions for better performance.", "Add type hints and modular documentation."],
            refactored_code=code_text
        )
