import logging
from typing import List
from backend.gemini_client import gemini_client
from backend.schemas.flashcard import FlashcardRequest, FlashcardResponse, FlashcardCard
from backend.utils.prompts import FLASHCARD_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def generate_flashcards(request: FlashcardRequest) -> FlashcardResponse:
    """
    Generates interactive flashcards for study revision.
    """
    topic = request.topic.strip()
    count = request.count
    prompt = FLASHCARD_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        topic=topic,
        count=count
    )

    try:
        raw_data = gemini_client.generate_json(prompt, temperature=0.5)
        
        cards_data = []
        if isinstance(raw_data, list):
            cards_data = raw_data
        elif isinstance(raw_data, dict):
            cards_data = raw_data.get("cards") or raw_data.get("flashcards") or list(raw_data.values())[0]

        parsed_cards: List[FlashcardCard] = []
        for item in cards_data:
            if not isinstance(item, dict):
                continue
            term = str(item.get("term") or item.get("question") or "").strip()
            defn = str(item.get("definition") or item.get("answer") or "").strip()
            ex = str(item.get("example") or "").strip()

            if term and defn:
                parsed_cards.append(FlashcardCard(term=term, definition=defn, example=ex))

        # Fallback if empty
        if not parsed_cards:
            parsed_cards = [
                FlashcardCard(
                    term=f"Core Concept of {topic}",
                    definition=f"The primary foundational principle behind {topic}.",
                    example="Key application in study."
                ),
                FlashcardCard(
                    term=f"Key Mechanism in {topic}",
                    definition=f"How elements interact within {topic}.",
                    example="Practical scenario."
                ),
                FlashcardCard(
                    term=f"Important Terminology: {topic}",
                    definition=f"Essential vocabulary required to master {topic}.",
                    example="Standard definition."
                )
            ]

        return FlashcardResponse(topic=topic, cards=parsed_cards)

    except Exception as err:
        logger.error(f"Error generating flashcards: {err}")
        return FlashcardResponse(
            topic=topic,
            cards=[
                FlashcardCard(
                    term=f"Introduction to {topic}",
                    definition=f"Foundational understanding of {topic}.",
                    example="Beginner flashcard study item."
                ),
                FlashcardCard(
                    term=f"Core Principle of {topic}",
                    definition=f"Key rule or theorem defining {topic}.",
                    example="Study revision example."
                ),
                FlashcardCard(
                    term=f"Summary of {topic}",
                    definition=f"Main takeaway for exam review.",
                    example="Key concept."
                )
            ]
        )
