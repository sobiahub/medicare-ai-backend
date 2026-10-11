import os

from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

load_dotenv(os.path.join(BASE_DIR, ".env"))

MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")

if not MONGO_URI:
    raise ValueError("MONGO_URI is missing from .env")

if not MONGO_DB_NAME:
    raise ValueError("MONGO_DB_NAME is missing from .env")


client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=5000,
)

db = client[MONGO_DB_NAME]


def check_mongodb_connection():
    try:
        client.admin.command("ping")
        print("MongoDB connected successfully!")
        print(f"Database: {MONGO_DB_NAME}")
        return True

    except ConnectionFailure as error:
        print(f"MongoDB connection failed: {error}")
        return False