from unittest.mock import patch

def test_flashcards_endpoint(client):
    mock_cards = [
        {"term": "Term 1", "definition": "Def 1", "example": "Ex 1"},
        {"term": "Term 2", "definition": "Def 2", "example": "Ex 2"},
        {"term": "Term 3", "definition": "Def 3", "example": "Ex 3"}
    ]
    with patch("backend.modules.flashcard.gemini_client.generate_json", return_value=mock_cards):
        response = client.post("/flashcards", json={"topic": "Physics", "count": 3})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Physics"
        assert len(data["cards"]) >= 3

def test_code_explain_endpoint(client):
    mock_explain = {
        "summary": "Binary search algorithm.",
        "time_complexity": "O(log N)",
        "space_complexity": "O(1)",
        "line_by_line": [{"line_or_section": "1-5", "explanation": "Loop logic"}],
        "optimizations": ["Use mid = low + (high - low) // 2"],
        "refactored_code": "def binary_search()..."
    }
    with patch("backend.modules.code_explainer.gemini_client.generate_json", return_value=mock_explain):
        response = client.post("/code-explain", json={"code_or_topic": "def search(): pass", "language": "Python"})
        assert response.status_code == 200
        data = response.json()
        assert data["time_complexity"] == "O(log N)"
        assert len(data["line_by_line"]) > 0

def test_mindmap_endpoint(client):
    mock_nodes = {
        "topic": "AI",
        "nodes": [
            {"id": "root", "label": "AI", "description": "Root", "parent_id": None},
            {"id": "ml", "label": "Machine Learning", "description": "Sub", "parent_id": "root"}
        ]
    }
    with patch("backend.modules.mindmap.gemini_client.generate_json", return_value=mock_nodes):
        response = client.post("/mindmap", json={"topic": "AI"})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "AI"
        assert len(data["nodes"]) == 2

def test_study_plan_endpoint(client):
    mock_plan = {
        "topic": "Calculus",
        "total_days": 3,
        "strategy_overview": "Daily limits",
        "schedule": [
            {"day": 1, "focus_area": "Limits", "tasks": ["Read Ch 1"], "break_strategy": "25/5"}
        ]
    }
    with patch("backend.modules.study_plan.gemini_client.generate_json", return_value=mock_plan):
        response = client.post("/study-plan", json={"exam_or_topic": "Calculus", "days_remaining": 3, "hours_per_day": 2.0})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Calculus"
        assert len(data["schedule"]) >= 1
