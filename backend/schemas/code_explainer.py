from typing import List, Optional
from pydantic import BaseModel, Field

class CodeExplainRequest(BaseModel):
    code_or_topic: str = Field(..., min_length=3, description="Code snippet or algorithm concept to explain.")
    language: str = Field(default="python", description="Programming language (e.g. Python, JavaScript, C++, SQL).")

class LineExplanation(BaseModel):
    line_or_section: str = Field(..., description="Line number or code chunk.")
    explanation: str = Field(..., description="Explanation of what this code does.")

class CodeExplainResponse(BaseModel):
    summary: str = Field(..., description="High-level overview of the code or algorithm.")
    time_complexity: str = Field(..., description="Big-O Time Complexity (e.g. O(N log N)).")
    space_complexity: str = Field(..., description="Big-O Space Complexity (e.g. O(1)).")
    line_by_line: List[LineExplanation] = Field(default_factory=list, description="Detailed line-by-line breakdown.")
    optimizations: List[str] = Field(default_factory=list, description="Optimization tips or bug fixes.")
    refactored_code: Optional[str] = Field(None, description="Improved, clean code version.")
