from fastapi.testclient import TestClient
from server.server import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}

def test_name_root():
    response = client.get("/name")
    assert response.status_code == 200
    assert response.json() == {"name": "name"}
