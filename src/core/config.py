from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MONGO_URL: str = "mongodb://127.0.0.1:27017"
    DB_NAME: str = "product_db"
    APP_NAME: str = "FastAPI App"
    DEBUG: bool = True

    model_config = {
        "env_file": ".env"
    }

settings = Settings()
