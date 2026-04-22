from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_pages_not_found():
    response = client.get("/pages/this-slug-does-not-exist-12345")
    assert response.status_code == 404
