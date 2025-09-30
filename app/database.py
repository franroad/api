# Import the create_engine function from SQLAlchemy, which is used to establish a connection to your database.
from sqlalchemy import create_engine

# Import declarative_base from SQLAlchemy's extension module.
# This function creates a base class that your ORM (Object Relational Mapping) model classes will inherit from.
from sqlalchemy.ext.declarative import declarative_base

# Import sessionmaker from SQLAlchemy's ORM module.
# sessionmaker is a factory function that generates new Session objects to interact with the database.
from sqlalchemy.orm import sessionmaker
from .config import settings

# Define the connection URL for your PostgreSQL database.
# Replace 'username', 'password', 'localhost', '5432', and 'database_name' with your actual PostgreSQL credentials and details.


# Creates a new SQLAlchemy Engine instance using the connection URL defined in SQLALCHEMY_DATABASE_URL.
# The engine is responsible for managing connections to your PostgreSQL database,
# including handling the connection pool, executing SQL statements, and managing overall communication with the database.
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)

SessionLocal=sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
