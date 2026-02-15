from fastapi.testclient import TestClient
from app.main import app
from app import schemas

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
    #assert response.json().get("email")=="test_user@pytest.com"
    #validating the response using response schema:
    new_user=schemas.UserResponse(**response.json())
    assert new_user.email=="test_user@pytest.com"
    
    print(response,response.json())