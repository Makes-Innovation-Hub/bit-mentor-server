from pymongo import MongoClient

from constants import CATEGORIES
from setting.config import config
from server.utils.logger import app_logger


def get_db():
    """

    :return: The YouTubeService instance used to interact with MongoDB
    """
    return youtube_mongo


class YouTubeService:

    def __init__(self):
        self.client = check_mongo_connection()
        self.db = self.client["youtube"]
        self.youtube_links_collection = self.db["youtube_links"]
        self.user_watched_links_collection = self.db["user_watched_links"]
        self.initialize_collections()
        # self.initialize_user("test_user1")
        self.add_fake_urls_to_python()

    def initialize_collections(self):
        """
        Initializes the collections for each category in CATEGORIES, creating an entry if it doesn't already exist.
        READ README TO KNOW THE STRUCTURE WITH EXAMPLE
        """
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
            app_logger.info(f"Collection for topic '{category}' initialized.")

    def initialize_user(self, user_id: str):
        """
        Initializes a user's watched video data if it doesn't already exist in the database.
        """
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
            app_logger.info(f"User data initialized for user_id '{user_id}'.")
            return user_data

    def add_fake_urls_to_python(self):  # avoid duplicate
        fake_urls = [f"https://www.youtube.com/watch?v=fake{i}" for i in range(1, 21)]
        for url in fake_urls:
            self.youtube_links_collection.update_one(
                {"topic": "Python"},
                {"$addToSet": {"length.short": url}},
                upsert=True
            )
        return {"message": "Fake URLs added successfully"}

    def find_youtube_links_by_topic_and_length(self, topic: str, length: str):
        """
            Retrieves YouTube links for a specific topic and length from the database.
        """
        document = self.youtube_links_collection.find_one({'topic': topic})
        urls = []
        for url in document["length"][length]:
            urls.append(url)
        app_logger.info(f"Retrieved {len(urls)} URLs for topic '{topic}' and length '{length}'.")
        return urls

    def link_exists_in_user_watched(self, user_id: str, topic: str, length: str, video_url: str) -> bool:
        """
        Checks if a user has already watched a specific YouTube video.
        :return: bool: True if the user has watched the video, False otherwise.
        """
        user_data = self.user_watched_links_collection.find_one({"user_id": user_id})
        if user_data and video_url in user_data["watched"][topic]["length"][length]:
            app_logger.info(f"Video URL '{video_url}' has already been watched by user_id '{user_id}'.")
            return True
        app_logger.info(f"Video URL '{video_url}' has not been watched by user_id '{user_id}'.")
        return False

    def update_user_stats(self, user_id: str, topic: str, length: str, video_url: str) -> bool:
        """
        :return: Updates the user's watched videos in the database by adding a new video URL.
        """
        update_result = self.user_watched_links_collection.update_one(
            {"user_id": user_id},
            {"$push": {f"watched.{topic}.length.{length}": video_url}}
        )
        if update_result.modified_count > 0:
            app_logger.info(f"User stats updated for user_id '{user_id}', topic '{topic}', length '{length}', with video URL '{video_url}'.")
            return True
        else:
            app_logger.error(f"Failed to update user stats for user_id '{user_id}', topic '{topic}', length '{length}', with video URL '{video_url}'.")
            return False


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
