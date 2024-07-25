import pymongo
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()


def get_db():
    return MongoDatabase()


class MongoDatabase:
    def __init__(self):
        self.client = check_mongo_connection()
        self.db = self.client["QuestDB"]
        self.questions_collection = self.db["Questions"]
        self.users_collection = self.db["Users"]
        self.topics_collection = self.db["Topics"]


def check_mongo_connection():
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    cluster_url = os.getenv("MONGO_CLUSTER_URL")
    if not all([username, password, cluster_url]):
        raise KeyError("MongoDB credentials are not set/loaded correctly.")

    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}"
    print(connection_string)
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return {"status": "Connection to MongoDB successful!"}
    except Exception as e:
        return {"error": str(e)}