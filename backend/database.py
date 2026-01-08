import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
MONGODB_DB_NAME = os.getenv("MONGODB_DB_NAME", "perplexiplay")

client = AsyncIOMotorClient(MONGODB_URL)
db = client[MONGODB_DB_NAME]

async def get_db():
    """Dependency to get the MongoDB database collection."""
    return db
