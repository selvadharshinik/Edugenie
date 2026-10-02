from typing import List
from pydantic import BaseModel, Field

class StudyPlanRequest(BaseModel):
    exam_or_topic: str = Field(..., min_length=2, description="Exam or subject to study.")
    days_remaining: int = Field(default=7, ge=1, le=30, description="Days available until exam (1 to 30).")
    hours_per_day: float = Field(default=2.0, ge=0.5, le=12.0, description="Study hours per day.")

class StudyDay(BaseModel):
    day: int = Field(..., description="Day number (1, 2, 3...).")
    focus_area: str = Field(..., description="Main subject/topic focus for this day.")
    tasks: List[str] = Field(..., description="Actionable tasks to complete.")
    break_strategy: str = Field(default="Pomodoro (25m study / 5m break)", description="Recommended study pacing.")

class StudyPlanResponse(BaseModel):
    topic: str = Field(..., description="Exam or subject name.")
    total_days: int = Field(..., description="Total days in plan.")
    strategy_overview: str = Field(..., description="High-level revision strategy.")
    schedule: List[StudyDay] = Field(..., description="Daily study schedule.")
