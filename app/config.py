from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SQLALCHEMY_DATABASE_URL:str
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



settings=Settings()


