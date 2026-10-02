import logging
from typing import List, Dict, Any
from backend.gemini_client import gemini_client
from backend.schemas.learning_path import (
    LearningPathRequest,
    LearningPathResponse,
    LearningStage,
)
from backend.utils.prompts import LEARNING_PATH_PROMPT, SYSTEM_PROMPT_BASE

logger = logging.getLogger(__name__)

def generate_learning_path(request: LearningPathRequest) -> LearningPathResponse:
    """
    Generates a structured learning path with Beginner, Intermediate, and Advanced stages.
    """
    topic = request.topic.strip()
    prompt = LEARNING_PATH_PROMPT.format(
        system_base=SYSTEM_PROMPT_BASE,
        topic=topic
    )

    try:
        raw_data = gemini_client.generate_json(prompt, temperature=0.5)
        
        stages_data = []
        if isinstance(raw_data, dict):
            stages_data = raw_data.get("stages", [])
        elif isinstance(raw_data, list):
            stages_data = raw_data

        parsed_stages: List[LearningStage] = []
        levels = ["Beginner", "Intermediate", "Advanced"]

        for idx, stage_dict in enumerate(stages_data[:3]):
            if not isinstance(stage_dict, dict):
                continue
            
            level_name = stage_dict.get("level", levels[idx] if idx < 3 else "Advanced")
            title = stage_dict.get("title", f"{level_name} Foundations in {topic}")
            description = stage_dict.get("description", f"Master core concepts for {level_name} level.")
            topics = stage_dict.get("topics", [f"{topic} Basics"])
            concepts = stage_dict.get("concepts", ["Core Fundamentals"])
            activities = stage_dict.get("practical_activities", ["Hands-on Practice"])
            resources = stage_dict.get("resources", ["Official Documentation & Tutorials"])

            parsed_stages.append(
                LearningStage(
                    level=level_name,
                    title=title,
                    description=description,
                    topics=topics if isinstance(topics, list) else [str(topics)],
                    concepts=concepts if isinstance(concepts, list) else [str(concepts)],
                    order=idx + 1,
                    practical_activities=activities if isinstance(activities, list) else [str(activities)],
                    resources=resources if isinstance(resources, list) else [str(resources)]
                )
            )

        # Fallback if stages were incomplete
        while len(parsed_stages) < 3:
            idx = len(parsed_stages)
            lvl = levels[idx]
            parsed_stages.append(
                LearningStage(
                    level=lvl,
                    title=f"{lvl} {topic} Mastery",
                    description=f"Explore and apply {lvl.lower()} concepts in {topic}.",
                    topics=[f"{lvl} {topic} Core"],
                    concepts=[f"{lvl} Principles"],
                    order=idx + 1,
                    practical_activities=[f"Complete a {lvl.lower()} project"],
                    resources=["Recommended Textbooks & Guides"]
                )
            )

        return LearningPathResponse(topic=topic, stages=parsed_stages)

    except Exception as err:
        logger.error(f"Error generating learning path: {err}")
        # Return structured fallback response
        return LearningPathResponse(
            topic=topic,
            stages=[
                LearningStage(
                    level="Beginner",
                    title=f"Introduction to {topic}",
                    description=f"Build a strong foundational understanding of {topic}.",
                    topics=[f"What is {topic}?", "Basic Terminology", "Key Principles"],
                    concepts=["Fundamentals", "Core Syntax / Rules"],
                    order=1,
                    practical_activities=["Simple guided exercises", "Basic flashcard review"],
                    resources=["Beginner Documentation", "Introductory Video Courses"]
                ),
                LearningStage(
                    level="Intermediate",
                    title=f"Practical {topic} Application",
                    description=f"Apply {topic} to solve real-world problems and build projects.",
                    topics=["Intermediate Workflows", "Best Practices", "Common Patterns"],
                    concepts=["Modularity", "Optimization Basics"],
                    order=2,
                    practical_activities=["Build a mini-project", "Solve practice problems"],
                    resources=["Official Guides", "Interactive Tutorials"]
                ),
                LearningStage(
                    level="Advanced",
                    title=f"Mastery & Deep Dive in {topic}",
                    description=f"Explore complex topics, optimization, and expert-level concepts.",
                    topics=["Architecture", "Advanced Techniques", "Performance Tuning"],
                    concepts=["Scalability", "Expert Paradigms"],
                    order=3,
                    practical_activities=["Design end-to-end system", "Contribute to open topics"],
                    resources=["Advanced Textbooks", "Research Papers & Case Studies"]
                )
            ]
        )
