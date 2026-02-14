from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

#Test the hello world
def test_hello_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 😬"}
    print(response, response.json()) # print(response, response.json().get("message"))

def test_create_user():
    response=client.post("user/add",json={"email":"test_user@pytest.com","password":"1231"}) # sending data in the body, we pass a dictionary
    assert response.status_code==201
    print(response,response.json())