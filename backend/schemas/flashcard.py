from typing import List
from pydantic import BaseModel, Field

class FlashcardRequest(BaseModel):
    topic: str = Field(..., min_length=2, description="Topic or content to generate flashcards from.")
    count: int = Field(default=5, ge=3, le=10, description="Number of flashcards (3 to 10).")

class FlashcardCard(BaseModel):
    term: str = Field(..., description="Front of card: concept or question.")
    definition: str = Field(..., description="Back of card: detailed definition or answer.")
    example: str = Field(default="", description="Optional real-world example.")

class FlashcardResponse(BaseModel):
    topic: str = Field(..., description="Topic of the flashcard deck.")
    cards: List[FlashcardCard] = Field(..., description="List of generated flashcards.")
