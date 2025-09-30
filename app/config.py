from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    testenv:str

    class Config:
        env_file= ".env"


settings=Settings()


