import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_db():
    return MongoDatabase()


class MongoDatabase:
    def __init__(self):
        self.client = _check_mongo_connection()
        self.db = self.client["QuestDB"]
        self.questions_collection = self.db["Questions"]
        self.users_collection = self.db["Users"]
        self.topics_collection = self.db["Topics"]


def _check_mongo_connection():
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    cluster_url = os.getenv("MONGO_CLUSTER_URL")

    if not all([username, password, cluster_url]):
        raise EnvironmentError("MongoDB credentials are not set.")

    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}"
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return client
    except Exception as e:
        raise ConnectionError(f"Failed to connect to MongoDB: {str(e)}")
