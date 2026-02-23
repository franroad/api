from app import schemas
from .database import client
from .database import db_test

    
    
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

def test_user_login(client):
    response=client.post("/auth",data={"username": "test_user@pytest.com", "password": "1231"})
    token=schemas.Token(**response.json())
    assert response.status_code==200
    assert token.access_token is not None


    


