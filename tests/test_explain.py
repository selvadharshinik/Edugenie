from unittest.mock import patch

def test_explain_endpoint_success(client):
    """Test POST /explain with valid topic."""
    mock_explanation = "Quantum computing uses qubits to process complex computations simultaneously."
    with patch("backend.modules.explanation.gemini_client.generate_text", return_value=mock_explanation):
        response = client.post("/explain", json={"topic": "Quantum Computing"})
        assert response.status_code == 200
        data = response.json()
        assert data["topic"] == "Quantum Computing"
        assert "explanation" in data
        assert data["explanation"] == mock_explanation

def test_explain_endpoint_empty(client):
    """Test POST /explain with empty topic."""
    response = client.post("/explain", json={"topic": ""})
    assert response.status_code == 422
