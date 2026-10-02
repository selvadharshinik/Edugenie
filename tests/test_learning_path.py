from unittest.mock import patch

MOCK_LEARNING_PATH_JSON = {
    "topic": "Python Programming",
    "stages": [
        {
            "level": "Beginner",
            "title": "Python Fundamentals",
            "description": "Learn syntax, variables, and loops.",
            "topics": ["Variables", "Control Flow"],
            "concepts": ["Syntax"],
            "order": 1,
            "practical_activities": ["Write print scripts"],
            "resources": ["Python Official Tutorial"]
        },
        {
            "level": "Intermediate",
            "title": "Data Structures & OOP",
            "description": "Master lists, dicts, classes, and modules.",
            "topics": ["OOP", "File I/O"],
            "concepts": ["Classes", "Inheritance"],
            "order": 2,
            "practical_activities": ["Build CLI app"],
            "resources": ["Real Python Guides"]
        },
        {
            "level": "Advanced",
            "title": "Advanced Frameworks & Design",
            "description": "FastAPI, async programming, and optimization.",
            "topics": ["AsyncIO", "FastAPI"],
            "concepts": ["Concurrency"],
            "order": 3,
            "practical_activities": ["Deploy web service"],
            "resources": ["FastAPI Documentation"]
        }
    ]
}

def test_learning_path_endpoint_success(client):
    """Test POST /learn/recommendations endpoint structure."""
    with patch("backend.modules.learning_path.gemini_client.generate_json", return_value=MOCK_LEARNING_PATH_JSON):
        response = client.post("/learn/recommendations", json={"topic": "Python Programming"})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Python Programming"
        assert "stages" in data
        assert len(data["stages"]) == 3
        levels = [s["level"] for s in data["stages"]]
        assert levels == ["Beginner", "Intermediate", "Advanced"]

def test_learning_path_endpoint_empty(client):
    """Test POST /learn/recommendations with empty input."""
    response = client.post("/learn/recommendations", json={"topic": ""})
    assert response.status_code == 422
