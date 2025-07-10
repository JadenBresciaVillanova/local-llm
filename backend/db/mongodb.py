# # backend/db/mongodb.py
# import os
# from motor.motor_asyncio import AsyncIOMotorClient

# # --- MongoDB Configuration ---
# MONGO_USER = os.getenv("MONGO_INITDB_ROOT_USERNAME", "mongo")
# MONGO_PASSWORD = os.getenv("MONGO_INITDB_ROOT_PASSWORD", "mongo_pass")
# MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
# MONGO_PORT = os.getenv("MONGO_PORT", "27017")

# MONGO_DETAILS = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}"

# class MongoDB:
#     client: AsyncIOMotorClient = None

# db_client = MongoDB()

# async def get_mongo_db():
#     return db_client.client.app_db # Return the database object

# def connect_to_mongo():
#     print("Connecting to MongoDB...")
#     db_client.client = AsyncIOMotorClient(MONGO_DETAILS)
#     print("Successfully connected to MongoDB.")

# def close_mongo_connection():
#     print("Closing MongoDB connection...")
#     db_client.client.close()
#     print("MongoDB connection closed.")

import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URL = os.getenv("MONGO_URL", "mongodb://myuser:supersecret@mongo:27017/")
MONGO_DB_NAME = "rag_app_db" # Name for your application's database

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