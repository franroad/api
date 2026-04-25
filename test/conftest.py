# Config file from pytest
# Makes fixtures and tests (functions) available for the package(test) 

#THIS SECTION IS EXECUTED BY RUNING PYTEST COMMAND
#BY LEVERAGING THE OVERRIDE DATABASE

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings,settings_test
from app.database import get_db
import pytest
from app.database import Base
from sqlalchemy import inspect,insert
from alembic import command
from app import schemas,models
import jwt
from app.oauth import create_access_token
from test.test_users import test_user_login

#engine = create_engine (settings.SQLALCHEMY_DATABASE_URL)
# engine = create_engine(f'{settings.SQLALCHEMY_DATABASE_URL}_test') #Crea el motor (responsable conexion) de SQL ALCHEMY pero no lo ejecuta
engine =create_engine( f"postgresql+psycopg2://{settings_test.DDBB_USER}:{settings_test.DDBB_PASSWORD}@localhost:{settings_test.DDBB_PORT_HOST}/{settings_test.DDBB_NAME}")


TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)#(SessionFactory)Asocia motor y sesion , permite crear sesiones usando el motor.

#Base.metadata.create_all(bind=engine) #redundant because of fixture


# With the fixture config we can access to the client(HTTP) but also to the DDBB (get_db_test)
# Fixture que prepara una base de datos limpia para cada test y crea la conexion
@pytest.fixture#(scope="module")
def db_test(): 
    # Elimina todas las tablas del motor de pruebas
    Base.metadata.drop_all(bind=engine)

    # Crea todas las tablas nuevamente (base de datos limpia)
    Base.metadata.create_all(bind=engine)

    # Crea una sesión de SQLAlchemy usando la configuración de pruebas (llama al SessionFactory)
    db = TestingSessionLocal()

    try:
        # Entrega la sesión al test que la necesite
        # El test usará esta sesión como si fuera la real
        yield db
    finally:
        # Cuando el test termina, se cierra la sesión
        db.close()



# Funcion de TestClient
client = TestClient(app)#Crea un cliente HTTP(TestClient) que permite hacer peticiones a la aplicación FastAPI sin necesidad de levantar un servidor real.

# Fixture que crea un TestClient pero usando la base de datos de pruebas
@pytest.fixture
def client(db_test): # Recibe la session de pruebas (por el yield) ↑↑↑↑
    # Esta función reemplaza la dependencia get_db de FastAPI
    def override_get_db():
        
            yield db_test

    # Sobrescribimos la dependencia original de FastAPI
    # Ahora cada vez que un endpoint llame a get_db, usará override_get_db
    app.dependency_overrides[get_db] = override_get_db

    # Devolvemos un TestClient que ya está configurado para usar la DB de pruebas
    yield TestClient(app)



@pytest.fixture
#Generating user after clearing database
def generate_user(client):
    new_data={"email":"test_user@fixture.com","password":"1231"} # This is a DICT
    response=client.post("user/add",json=(new_data))
    new_user=response.json() # This response is also a dict
    print (f"USER_ADD:  {response.json()}")
    new_user['password']=new_data['password'] #Estamos haciendo un append anadiendo una key "password"
    return new_user #as we are not using pydantic
                    # this is returning everything but not the id



@pytest.fixture
def fixture_login(client, generate_user):
    response=client.post("/auth",data={"username": generate_user['email'], "password": generate_user['password']})
    
    token=schemas.Token(**response.json())
    #print(f"info: {generate_user['email'],generate_user['password']}")
    assert response.status_code==200
    # Validate the Token
    payload = jwt.decode(token.access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    id=payload.get("user_id")
    
    print(f"Fixture user_id: {id}")
    return id # with an existing id , we can create the token below:
    


#Create "Fake access token"
@pytest.fixture
def test_token(fixture_login): #we can use any id int as is not validated 
    return create_access_token({"user_id":fixture_login})

#We only need to add the token for the protected routes as in posman
@pytest.fixture
def authorized_client(client,test_token):
    client.headers={
        **client.headers,
        "Authorization": f"Bearer {test_token}"
    }
    
    return client

# useful for voting and update post amongt others
@pytest.fixture
def test_create_posts(fixture_login,db_test):
    posts_data=[{ # THIS IS A LIST OF DICTIONARIES FULL PYTHON
        "title": "first title",
        "content":"first content",
        "user_id":fixture_login

    },{
        "title": "first title",
        "content":"2nd content",
        "user_id":fixture_login


    },{
        "title": "first title",
        "content":"3rd content",
        "user_id":fixture_login
    }]

    # TRANSFORMATION INTO ORM OBJECT and creates a list
    ## with ** it picks each key and value for inserting in the table



    new_test_posts=[models.PostORM(**post)for post in posts_data] 

    # another example
    # posts_list=[]
    # for post in posts_data:
    #     posts_list.append(models.PostORM(**post))



    db_test.add_all(new_test_posts)
    db_test.commit()
    
    posts=db_test.query(models.PostORM).all()
    return posts