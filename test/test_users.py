#THIS SECTION IS EXECUTED BY RUNING PYTEST COMMAND
#BY LEVERAGING THE OVERRIDE DATABASE

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app import schemas
from app.config import settings
from app.database import get_db
import pytest
from app.database import Base
from sqlalchemy import inspect
from alembic import command

#engine = create_engine (settings.SQLALCHEMY_DATABASE_URL)
engine = create_engine(f'{settings.SQLALCHEMY_DATABASE_URL}_test') #Crea el motor (responsable conexion) de SQL ALCHEMY pero no lo ejecuta
#engine =create_engine( f"postgresql+psycopg2://{settings.DDBB_USER}:{settings.DDBB_PASSWORD}@{settings.DDBB_HOSTNAME}:{settings.DDBB_PORT}/{settings.DDBB_NAME}")

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)#Asocia motor y sesion , permite crear sesiones usando el motor.

#Base.metadata.create_all(bind=engine) #redundant because of fixture


def get_db_test():
    db=TestingSessionLocal() #Crea la session
    try:
        yield db #Cuando endpoint finaliza FastAPI reanuda get_db() después del yield
    finally:
        db.close() #Cierra la sesion

app.dependency_overrides[get_db]=get_db_test


client = TestClient(app)#Crea un cliente HTTP(TestClient) que permite hacer peticiones a la aplicación FastAPI sin necesidad de levantar un servidor real.

@pytest.fixture
def clean_ddbb():
    #command.upgrade("head") # To use alembic instead of sql alchemy.
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield TestClient(app)
    #command.upgrade("base") # To use alembic instead of sql alchemy.
    


#Test the hello world
def test_hello_main(clean_ddbb):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World 😬"}
    print(response, response.json()) # print(response, response.json().get("message"))



def test_create_user(clean_ddbb):
    response=client.post("user/add",json={"email":"test_user@pytest.com","password":"1231"}) # sending data in the body, we pass a dictionary
    if response.status_code !=201:
        print(f"status code: {response.status_code}, detail: {response.json().get('detail')}")
    
    assert response.status_code==201
    #assert response.json().get("email")=="test_user@pytest.com"
    #validating the response using response schema:
    new_user=schemas.UserResponse(**response.json())
    assert new_user.email=="test_user@pytest.com"
    
    print(response, response.json())