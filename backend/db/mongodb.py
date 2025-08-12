import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://myuser:supersecret@mongo:27017/")
MONGO_DB_NAME = "rag_app_db" 

class MongoManager:
    client: AsyncIOMotorClient = None
    database = None

db = MongoManager()

async def connect_to_mongo():
    print("Connecting to MongoDB...")
    db.client = AsyncIOMotorClient(MONGO_URL)
    db.database = db.client[MONGO_DB_NAME]
    print("Successfully connected to MongoDB.")

async def close_mongo_connection():
    print("Closing MongoDB connection...")
    if db.client:
        db.client.close()
    print("MongoDB connection closed.")

def get_mongo_db():
    # This is a synchronous function that returns the database object
    # that was initialized at startup.
    if db.database is None:
        # This should ideally not happen if the lifespan manager is correct
        raise Exception("MongoDB has not been initialized.")
    return db.database