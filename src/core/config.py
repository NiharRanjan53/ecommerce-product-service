from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://127.0.0.1:27017"
    DB_NAME: str = "product_db"
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True

    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256" 
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM:str
    MAIL_PORT:int
    MAIL_SERVER:str


    model_config = {
        "env_file": ".env"
    }

settings = Settings()
