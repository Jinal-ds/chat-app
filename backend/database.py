from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from models.user import User
from models.room import Room
from models.message import Message
from config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGO_URL)
    await init_beanie(
        database=client[settings.DB_NAME],
        document_models=[User, Room, Message]
    )