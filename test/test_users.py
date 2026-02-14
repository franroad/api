from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Test the hello world
def test_hello_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 😬"}