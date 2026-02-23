from app import schemas
from app.config import settings
from .database import client
from .database import db_test
import pytest,jwt

@pytest.fixture
def generate_user(client):
    new_data={"email":"test_user@fixture.com","password":"1231"} # This is a DICT
    response=client.post("user/add",json=(new_data))
    new_user=response.json() # This response is also a dict
    new_user['password']=new_data['password'] #Estamos haciendo un append anadiendo una key "password"
    return new_user

#With the fixture config we can access to the client(HTTP) but also to the DDBB (get_db_test)

#Test the hello world
# The fixtures run here (before each test)
def test_hello_main(client): #El valor que produce el yield de esta fixture se pasa como argumento al test.
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 😬"}
    print(response, response.json()) # print(response, response.json().get("message"))

# The fixtures run here (before each test)

def test_create_user(client):
    response=client.post("user/add",json={"email":"test_user@pytest.com","password":"1231"}) # sending data in the body, we pass a dictionary
    if response.status_code !=201:
        print(f"status code: {response.status_code}, detail: {response.json().get('detail')}")
    
    assert response.status_code==201
    #assert response.json().get("email")=="test_user@pytest.com"
    #validating the response using response schema:
    new_user=schemas.UserResponse(**response.json())
    assert new_user.email=="test_user@pytest.com"
    
    print(response, response.json())

# The fixtures run here (before each test)


def test_user_login(client,generate_user):
    response=client.post("/auth",data={"username": "test_user@fixture.com", "password": "1231"})
    token=schemas.Token(**response.json())
    print(f"info: {generate_user['email'],generate_user['password']}")
    assert response.status_code==200
    # Validate the Token
    payload = jwt.decode(token.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

    id=payload.get("user_id")
    print(f"user_id: {id}")
    assert id is not None




