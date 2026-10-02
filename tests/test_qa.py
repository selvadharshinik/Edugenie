from unittest.mock import patch
from backend.schemas.qa import QAResponse

def test_qa_endpoint_success(client):
    """Test POST /qa with valid question."""
    mock_answer = "Photosynthesis is the process by which plants convert light into energy."
    with patch("backend.modules.qna.gemini_client.generate_text", return_value=mock_answer):
        response = client.post("/qa", json={"question": "What is photosynthesis?"})
        assert response.status_code == 200
        data = response.json()
        assert "answer" in data
        assert data["answer"] == mock_answer

def test_qa_endpoint_validation_error(client):
    """Test POST /qa with invalid empty payload."""
    response = client.post("/qa", json={"question": ""})
    assert response.status_code == 422
