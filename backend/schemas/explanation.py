from pydantic import BaseModel, Field

class ExplainRequest(BaseModel):
    topic: str = Field(..., min_length=2, description="The topic to explain simply.")

class ExplainResponse(BaseModel):
    topic: str = Field(..., description="The original topic.")
    explanation: str = Field(..., description="Structured, beginner-friendly explanation text.")
