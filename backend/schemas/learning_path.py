from typing import List, Optional
from pydantic import BaseModel, Field

class LearningPathRequest(BaseModel):
    topic: str = Field(..., min_length=2, description="Topic for personalized learning path recommendations.")

class LearningStage(BaseModel):
    level: str = Field(..., description="Stage level: Beginner, Intermediate, or Advanced.")
    title: str = Field(..., description="Descriptive stage title.")
    description: str = Field(..., description="Overview of what the learner will master in this stage.")
    topics: List[str] = Field(default_factory=list, description="Specific topics covered.")
    concepts: List[str] = Field(default_factory=list, description="Key concepts to grasp.")
    order: int = Field(..., description="Sequence number (1, 2, or 3).")
    practical_activities: List[str] = Field(default_factory=list, description="Recommended exercises or projects.")
    resources: List[str] = Field(default_factory=list, description="Suggested learning resources, books, or documentation.")

class LearningPathResponse(BaseModel):
    topic: str = Field(..., description="The learning path topic.")
    stages: List[LearningStage] = Field(..., description="Progression of stages: Beginner, Intermediate, Advanced.")
