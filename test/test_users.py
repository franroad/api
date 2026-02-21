from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db

#engine = create_engine (settings.SQLALCHEMY_DATABASE_URL)
engine = create_engine(f'{settings.SQLALCHEMY_DATABASE_URL}_test')
#engine =create_engine( f"postgresql+psycopg2://{settings.DDBB_USER}:{settings.DDBB_PASSWORD}@{settings.DDBB_HOSTNAME}:{settings.DDBB_PORT}/{settings.DDBB_NAME}")

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()#contiene la info(metadata) de nuestros models en memoria , lo usa alembic para comparar con la DDBB

def test_get_db():
    db=TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db]=test_get_db








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