from pydantic import BaseModel, Field

class SummarizeRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Educational text to summarize.")

class SummarizeResponse(BaseModel):
    summary: str = Field(..., description="Concise educational summary.")
