from typing import List
from pydantic import BaseModel, Field, field_validator

class QuizRequest(BaseModel):
    text: str = Field(..., min_length=5, description="Text or topic to generate a quiz from.")

class QuizQuestion(BaseModel):
    question: str = Field(..., min_length=3, description="The question text.")
    options: List[str] = Field(..., description="List of 4 multiple-choice options.")
    answer: str = Field(..., description="The exact correct answer matching one of the options.")

    @field_validator('options')
    def validate_options_count(cls, v):
        if len(v) != 4:
            raise ValueError(f"Each quiz question must have exactly 4 options. Got {len(v)} options.")
        return v

    @field_validator('answer')
    def validate_answer_in_options(cls, v, info):
        options = info.data.get('options')
        if options and v not in options:
            # Check if trimmed answer matches trimmed option
            trimmed_options = [opt.strip() for opt in options]
            if v.strip() in trimmed_options:
                # Return matched exact option
                idx = trimmed_options.index(v.strip())
                return options[idx]
            raise ValueError(f"The correct answer '{v}' must be one of the listed options: {options}")
        return v

class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(..., description="List of exactly 3 quiz questions.")

    @field_validator('questions')
    def validate_questions_count(cls, v):
        if len(v) != 3:
            raise ValueError(f"Quiz must contain exactly 3 questions. Got {len(v)} questions.")
        return v
