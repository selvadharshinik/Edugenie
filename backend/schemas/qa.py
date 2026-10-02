from pydantic import BaseModel, Field

class QARequest(BaseModel):
    question: str = Field(..., min_length=2, description="The educational or academic question to ask.")

class QAResponse(BaseModel):
    answer: str = Field(..., description="Concise, contextual answer from EduGenie.")
