from unittest.mock import patch

def test_summarize_endpoint_success(client):
    """Test POST /summarize with educational text."""
    mock_summary = "Summary: Artificial intelligence is transforming education by enabling personalized learning."
    with patch("backend.modules.summary.gemini_client.generate_text", return_value=mock_summary):
        response = client.post("/summarize", json={"text": "Artificial intelligence is rapidly transforming the modern educational landscape..."})
        assert response.status_code == 200
        data = response.json()
        assert "summary" in data
        assert data["summary"] == mock_summary

def test_summarize_endpoint_short_input(client):
    """Test POST /summarize with too short input."""
    response = client.post("/summarize", json={"text": "Short"})
    assert response.status_code == 422
