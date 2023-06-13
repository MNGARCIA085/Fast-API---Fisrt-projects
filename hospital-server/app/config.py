from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Awesome API"
    admin_email: str = "some mail"
    DB_USER:str
    DB_URL:str
    DB_URL_TEST:str

    class Config:
        env_file = ".env"


settings = Settings()