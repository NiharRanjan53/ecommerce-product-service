from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from src.core.config import settings

class MongoDB:
    client: AsyncIOMotorClient | None = None

mongodb = MongoDB()

async def connect_db():
    mongodb.client = AsyncIOMotorClient(settings.MONGO_URL)
    print("✅ MongoDB connected")

async def close_db():
    if mongodb.client:
        mongodb.client.close()
        print("❌ MongoDB disconnected")

def get_db() -> AsyncIOMotorDatabase:
    """Dependency for FastAPI routes."""
    if mongodb.client is None:
        raise RuntimeError("MongoDB client is not initialized")
    return mongodb.client[settings.DB_NAME]
