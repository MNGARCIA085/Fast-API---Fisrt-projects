from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "some mail"
    DB_URI:str
    DB_NAME: str
    DB_URI_TEST:str 
    DB_NAME_TEST:str

    class Config:
        env_file = ".env"


settings = Settings()