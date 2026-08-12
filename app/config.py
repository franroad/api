from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DDBB_NAME : str = "False"
    DDBB_USER : str = "False"
    DDBB_PASSWORD : str = "False"
    DDBB_HOSTNAME : str = "False"
    DDBB_PORT : int = 5432
    SQLALCHEMY_DATABASE_URL : str
    ALEMBIC_DATABASE_URL: str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    MAIL_USERNAME : str
    MAIL_PASSWORD : str
    MAIL_FROM : str
    MAIL_PORT : str
    MAIL_SERVER : str
    MAIL_STARTTLS:str
    MAIL_SSL_TLS:str

    class Config:
        env_file= ".env"


class TestSettings(BaseSettings):

    
        DDBB_NAME : str = "False"
        DDBB_USER : str = "False"
        DDBB_PASSWORD : str = "False"
        DDBB_HOSTNAME : str = "False"
        DDBB_PORT : int = 5432
        DDBB_PORT_HOST: int = 5432
        SECRET_KEY : str
        ALGORITHM : str
        ACCESS_TOKEN_EXPIRE_MINUTES : int
        MAIL_USERNAME : str
        MAIL_PASSWORD : str
        MAIL_FROM : str
        MAIL_PORT : str
        MAIL_SERVER : str
        MAIL_STARTTLS:str
        MAIL_SSL_TLS:str
        
        class Config:
            env_file= ".env.test"

settings=Settings()

settings_test=TestSettings()


