from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_ingest_smoke():
    # Only test if the endpoint exists and returns 422 for bad data
    response = client.post("/ingest/run", json={})
    assert response.status_code == 422
