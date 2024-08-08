from fastapi.testclient import TestClient
from server.server import app  # make sure to import your FastAPI app

client = TestClient(app)
def test_get_quote_success():
    response = client.get("/quote/1")
    assert response.status_code == 200
    response_json = response.json()


    assert "quote" in response_json
    assert "author" in response_json
    assert "category" in response_json