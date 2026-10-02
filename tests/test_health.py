def test_health_check(client):
    """Test GET /health returns 200 OK and status ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_root_index_template(client):
    """Test GET / renders HTML frontend template."""
    response = client.get("/")
    assert response.status_code == 200
    assert "EduGenie" in response.text
