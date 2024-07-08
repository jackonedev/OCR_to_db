from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_greetings():
    response = client.get("/check")
    assert response.status_code == 200
    assert response.json() == {"message": "Hola mundo"}
