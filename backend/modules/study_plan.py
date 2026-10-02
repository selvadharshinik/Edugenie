import logging
from typing import List
from backend.gemini_client import gemini_client
from backend.schemas.study_plan import StudyPlanRequest, StudyPlanResponse, StudyDay
from backend.utils.prompts import STUDY_PLAN_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def generate_study_plan(request: StudyPlanRequest) -> StudyPlanResponse:
    """
    Generates a daily structured study schedule for exam preparation.
    """
    topic = request.exam_or_topic.strip()
    days = request.days_remaining
    hours = request.hours_per_day

    prompt = STUDY_PLAN_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        topic=topic,
        days_remaining=days,
        hours_per_day=hours
    )

    try:
        raw_data = gemini_client.generate_json(prompt, temperature=0.5)
        
        strategy = "Focus on high-yield core concepts, daily active recall testing, and spaced repetition."
        days_list = []

        if isinstance(raw_data, dict):
            strategy = raw_data.get("strategy_overview", strategy)
            days_list = raw_data.get("schedule", [])
        elif isinstance(raw_data, list):
            days_list = raw_data

        parsed_schedule: List[StudyDay] = []
        for idx, item in enumerate(days_list):
            if not isinstance(item, dict):
                continue
            day_num = int(item.get("day", idx + 1))
            focus = str(item.get("focus_area", f"Day {day_num} Topic")).strip()
            tasks_raw = item.get("tasks", [f"Review {topic} concepts"])
            break_strat = str(item.get("break_strategy", "Pomodoro (25m study / 5m break)")).strip()

            tasks = [str(t) for t in tasks_raw] if isinstance(tasks_raw, list) else [str(tasks_raw)]
            parsed_schedule.append(
                StudyDay(day=day_num, focus_area=focus, tasks=tasks, break_strategy=break_strat)
            )

        # Fallback if schedule incomplete
        while len(parsed_schedule) < days:
            idx = len(parsed_schedule) + 1
            parsed_schedule.append(
                StudyDay(
                    day=idx,
                    focus_area=f"Day {idx} Review & Practice: {topic}",
                    tasks=[f"Complete practice questions for Day {idx}", "Review flashcards & key formulas"],
                    break_strategy="Pomodoro 25m study / 5m break"
                )
            )

        return StudyPlanResponse(
            topic=topic,
            total_days=days,
            strategy_overview=strategy,
            schedule=parsed_schedule[:days]
        )

    except Exception as err:
        logger.error(f"Error generating study plan: {err}")
        schedule_fallback = [
            StudyDay(
                day=i + 1,
                focus_area=f"Phase {i + 1}: {topic} Essentials",
                tasks=[f"Study core definitions for Phase {i + 1}", "Solve 5 practice problems"],
                break_strategy="25m study / 5m break"
            ) for i in range(days)
        ]
        return StudyPlanResponse(
            topic=topic,
            total_days=days,
            strategy_overview=f"Personalized {days}-day study plan for {topic}.",
            schedule=schedule_fallback
        )
