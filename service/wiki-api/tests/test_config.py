from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_config():
    response = client.get("/config")
    assert response.status_code == 200
    data = response.json()
    assert "paths" in data
    assert "llm_provider" in data
    assert "llm_model" in data
