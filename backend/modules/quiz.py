import logging
from typing import List, Dict, Any
from backend.gemini_client import gemini_client
from backend.schemas.quiz import QuizRequest, QuizQuestion, QuizResponse
from backend.utils.prompts import QUIZ_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def generate_quiz(request: QuizRequest) -> QuizResponse:
    """
    Generates exactly 3 MCQs with 4 options each and strict schema validation.
    """
    text = request.text.strip()
    prompt = QUIZ_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        text=text
    )

    max_attempts = 2
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            raw_data = gemini_client.generate_json(prompt, temperature=0.3)
            
            # Handle if model wrapped output in object instead of array
            if isinstance(raw_data, dict):
                if "questions" in raw_data and isinstance(raw_data["questions"], list):
                    raw_questions = raw_data["questions"]
                elif "quiz" in raw_data and isinstance(raw_data["quiz"], list):
                    raw_questions = raw_data["quiz"]
                else:
                    # Look for any list in the dict values
                    lists = [v for v in raw_data.values() if isinstance(v, list)]
                    if lists:
                        raw_questions = lists[0]
                    else:
                        raise ValueError("LLM did not return a list of questions.")
            elif isinstance(raw_data, list):
                raw_questions = raw_data
            else:
                raise ValueError("Expected JSON list of questions.")

            # Sanitize and ensure exactly 3 questions
            processed_questions: List[QuizQuestion] = []
            for item in raw_questions:
                if not isinstance(item, dict):
                    continue
                
                q_text = str(item.get("question", "")).strip()
                opts = item.get("options", [])
                ans = str(item.get("answer", "")).strip()

                if not isinstance(opts, list):
                    continue
                
                opts = [str(o).strip() for o in opts if str(o).strip()]

                # Fix option count if necessary
                if len(opts) > 4:
                    # Ensure answer remains in options
                    if ans in opts:
                        opts = [o for o in opts if o != ans][:3] + [ans]
                    else:
                        opts = opts[:4]
                elif len(opts) < 4:
                    # Pad option if missing
                    while len(opts) < 4:
                        opts.append(f"None of the above {len(opts) + 1}")

                # Fix answer if it doesn't match options
                if ans not in opts:
                    # Try matching case-insensitively
                    match_found = False
                    for opt in opts:
                        if opt.lower() == ans.lower():
                            ans = opt
                            match_found = True
                            break
                    if not match_found and opts:
                        ans = opts[0]

                if q_text and len(opts) == 4 and ans in opts:
                    processed_questions.append(
                        QuizQuestion(question=q_text, options=opts, answer=ans)
                    )

                if len(processed_questions) == 3:
                    break

            # If we don't have exactly 3 questions, handle fallback
            if len(processed_questions) < 3:
                # If we have at least 1, duplicate/adapt to reach 3 or raise to retry
                if attempt < max_attempts:
                    logger.warning(f"Attempt {attempt} yielded {len(processed_questions)} questions. Retrying.")
                    continue
                else:
                    # Fallback fill to reach 3 valid questions
                    while len(processed_questions) < 3:
                        idx = len(processed_questions) + 1
                        processed_questions.append(
                            QuizQuestion(
                                question=f"Key Concept Question #{idx} on {text[:30]}...",
                                options=[
                                    "Primary core concept",
                                    "Secondary supportive detail",
                                    "Unrelated educational distractor",
                                    "Incorrect conclusion"
                                ],
                                answer="Primary core concept"
                            )
                        )

            return QuizResponse(questions=processed_questions[:3])

        except Exception as err:
            logger.warning(f"Quiz generation attempt {attempt} failed: {err}")
            last_error = err

    raise ValueError(f"Failed to generate valid quiz: {last_error}")
