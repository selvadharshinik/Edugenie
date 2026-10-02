from unittest.mock import patch

MOCK_QUIZ_JSON = [
    {
        "question": "What is the primary power house of the cell?",
        "options": ["Mitochondria", "Nucleus", "Ribosome", "Golgi Apparatus"],
        "answer": "Mitochondria"
    },
    {
        "question": "Which organelle contains genetic material DNA?",
        "options": ["Lysosome", "Nucleus", "Cytoplasm", "Endoplasmic Reticulum"],
        "answer": "Nucleus"
    },
    {
        "question": "Where does protein synthesis occur?",
        "options": ["Cell Wall", "Vacuole", "Ribosome", "Chloroplast"],
        "answer": "Ribosome"
    }
]

def test_quiz_endpoint_valid_structure(client):
    """
    Test POST /quiz strictly enforces:
    1. Exactly 3 questions
    2. Exactly 4 options per question
    3. Correct answer matches one option
    """
    with patch("backend.modules.quiz.gemini_client.generate_json", return_value=MOCK_QUIZ_JSON):
        response = client.post("/quiz", json={"text": "Cell Biology and Organelles"})
        assert response.status_code == 200
        data = response.json()
        assert "questions" in data
        questions = data["questions"]

        # 1. Exactly 3 questions
        assert len(questions) == 3

        for q in questions:
            assert "question" in q
            assert "options" in q
            assert "answer" in q

            # 2. Exactly 4 options per question
            assert len(q["options"]) == 4

            # 3. Correct answer matches one option
            assert q["answer"] in q["options"]

def test_quiz_endpoint_empty_input(client):
    """Test POST /quiz with short/invalid input."""
    response = client.post("/quiz", json={"text": "abc"})
    assert response.status_code == 422
