from pymongo import MongoClient

from constants import CATEGORIES
from setting.config import config


def get_db():
    return youtube_mongo


class YouTubeService:

    def __init__(self):
        self.client = check_mongo_connection()
        self.db = self.client["youtube"]
        self.youtube_links_collection = self.db["youtube_links"]
        self.user_watched_links_collection = self.db["user_watched_links"]
        self.initialize_collections()
        self.initialize_user("test_user1")
        self.add_fake_urls_to_python()

    def initialize_collections(self):
        for category in CATEGORIES:
            if not self.youtube_links_collection.find_one({"topic": category}):
                self.youtube_links_collection.insert_one({
                    "topic": category,
                    "length": {
                        "short": [],
                        "medium": [],
                        "long": []
                    }
                })

    def initialize_user(self, user_id: str):
        if not self.user_watched_links_collection.find_one({"user_id": user_id}):
            user_data = {
                "user_id": user_id,
                "watched": {
                    category: {
                        "length": {
                            "short": [],
                            "medium": [],
                            "long": []
                        }
                    } for category in CATEGORIES
                }
            }
            self.user_watched_links_collection.insert_one(user_data)
            return user_data

    def add_fake_urls_to_python(self):
        fake_urls = [f"https://www.youtube.com/watch?v=fake{i}" for i in range(1, 21)]
        self.youtube_links_collection.update_one(
            {"topic": "Python"},
            {"$push": {"length.short": {"$each": fake_urls}}},
            upsert=True
        )
        return {"message": "Fake URLs added successfully"}


def check_mongo_connection():
    if not config.MONGO_CONNECTION_STRING:
        raise KeyError("MongoDB connection string is not set/loaded correctly.")
    connection_string = config.MONGO_CONNECTION_STRING
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return client
    except Exception as e:
        return {"error": str(e)}


youtube_mongo = YouTubeService()
