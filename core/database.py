from pymongo import MongoClient
from pymongo.errors import PyMongoError

from core.config import settings

try:
    client = MongoClient(
        settings.MONGODB_URI,
        serverSelectionTimeoutMS=2000
    )
    database = client[settings.DATABASE_NAME]
    jobs_collection = database[settings.COLLECTION_NAME]
except (PyMongoError, Exception) as error:
    print(f"MongoDB client initialization warning: {error}")
    client = None
    database = None
    jobs_collection = None


def check_database_connection():
    if client is None:
        return False
    try:
        client.admin.command("ping")
        return True
    except PyMongoError:
        return False


def get_jobs_collection():
    return jobs_collection
