#THIS SECTION IS EXECUTED BY RUNING PYTEST COMMAND
#BY LEVERAGING THE OVERRIDE DATABASE

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.config import settings
from app.database import get_db
import pytest
from app.database import Base
from sqlalchemy import inspect
from alembic import command

#engine = create_engine (settings.SQLALCHEMY_DATABASE_URL)
engine = create_engine(f'{settings.SQLALCHEMY_DATABASE_URL}_test') #Crea el motor (responsable conexion) de SQL ALCHEMY pero no lo ejecuta
#engine =create_engine( f"postgresql+psycopg2://{settings.DDBB_USER}:{settings.DDBB_PASSWORD}@{settings.DDBB_HOSTNAME}:{settings.DDBB_PORT}/{settings.DDBB_NAME}")

TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)#(SessionFactory)Asocia motor y sesion , permite crear sesiones usando el motor.

#Base.metadata.create_all(bind=engine) #redundant because of fixture


# With the fixture config we can access to the client(HTTP) but also to the DDBB (get_db_test)
# Fixture que prepara una base de datos limpia para cada test y crea la conexion
@pytest.fixture
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
        try:
            # En lugar de devolver la sesión real, devolvemos la de pruebas
            yield db_test
        finally:
            # Cerramos la sesión cuando el endpoint termina
            db_test.close()

    # Sobrescribimos la dependencia original de FastAPI
    # Ahora cada vez que un endpoint llame a get_db, usará override_get_db
    app.dependency_overrides[get_db] = override_get_db

    # Devolvemos un TestClient que ya está configurado para usar la DB de pruebas
    yield TestClient(app)
