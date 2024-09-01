from motor.motor_asyncio import AsyncIOMotorClient
from app.core.config import settings

async def get_database() -> AsyncIOMotorClient:
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    return client[settings.DATABASE_NAME]

async def close_mongo_connection(db: AsyncIOMotorClient):
    db.client.close()