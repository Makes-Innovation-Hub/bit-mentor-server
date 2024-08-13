from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, PyMongoError
from server.utils.logger import app_logger
from model.insert_queries import *
import urllib.parse as UP
from setting.config import *

ALLOWED_TOPICS = ["python", "algorithms", "dbs", "system design", "sql"]


class MongoDatabase:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database_name = database_name
        self.db = self.client[database_name]
        self.questions_collection = self.db["Questions"]
        self.users_answers_collection = self.db["Users"]
        self.stats_collection = self.db["stats"]
        self.topics = self.db["allowed_topics"]
        self.init_topics()

    def init_topics(self):
        try:
            # Fetch existing topics
            existing_topics = self.topics.find({}, {"_id": 0, "name": 1})
            existing_topic_names = {topic["name"] for topic in existing_topics}

            # Determine missing topics
            missing_topics = [topic for topic in ALLOWED_TOPICS if topic not in existing_topic_names]

            # Insert missing topics
            if missing_topics:
                self.topics.insert_many([{"name": topic} for topic in missing_topics])
        except Exception as e:
            raise RuntimeError("Failed to initialize topics") from e

    def insert_question(self, collection_name, question_data):
        if not self.client:
            self.check_mongo_connection(self.uri, self.database_name)
        try:
            questions_collection = self.questions_collection
            return insert_data(questions_collection, collection_name, self.database_name, question_data)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
            raise Exception(f"An error occurred while inserting data: {e}")

    def update_user_stat(self, user_id, update_fields):
        self.stats_collection.update_one(
            {'user_id': user_id},
            {'$inc': update_fields},
            upsert=True
        )

    def save_user_answer(self, collection_name, user_answer):
        if not self.client:
            self.check_mongo_connection(self.uri, self.database_name)
        try:
            users_answers_collection = self.users_answers_collection
            return insert_data(users_answers_collection, collection_name, self.database_name, user_answer)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
            raise Exception(f"An error occurred while inserting data: {e}")

    def check_mongo_connection(self):
        try:
            self.client.admin.command('ismaster')
            app_logger.info(f"MongoDB connection to database '{self.database_name}' successful!")
            return {"message": f"MongoDB connection to database '{self.database_name}' successful!"}
        except ConnectionFailure as e:
            app_logger.error(f"MongoDB connection failed: {e}")
        except Exception as e:
            app_logger.error(f"An error occurred: {e}")

    def load_topics_from_mongo(self):
        """
        Load the list of allowed topics from MongoDB.

        Returns:
            List[dict]: A list of topics.

        Raises:
            RuntimeError: If there is an error loading the topics.
        """
        try:
            topics_cursor = self.topics.find({}, {"_id": 0, "name": 1})
            topics = [topic["name"] for topic in topics_cursor]
            app_logger.info(f"Loaded topics: {topics}")
            return topics
        except PyMongoError as e:
            app_logger.error(f"Error loading topics from MongoDB: {e}")
            raise RuntimeError("Failed to load topics from MongoDB") from e

    def insert_new_topic(self, topic_name):
        """
        Insert a new topic into the allowed_topics collection if it doesn't already exist.

        Args:
            topic_name (str): The name of the topic to insert.

        Returns:
            dict: A message indicating the result of the operation.

        Raises:
            RuntimeError: If there is an error inserting the topic.
        """
        try:
            # Check if the topic already exists
            if self.topics.find_one({"name": topic_name}):
                app_logger.info(f"Topic '{topic_name}' already exists in the database.")
                return {"message": f"Topic '{topic_name}' already exists."}

            # Insert the new topic
            self.topics.insert_one({"name": topic_name})
            app_logger.info(f"Inserted new topic '{topic_name}' into the database.")
            return {"message": f"Topic '{topic_name}' successfully inserted."}

        except PyMongoError as e:
            app_logger.error(f"Error inserting topic into MongoDB: {e}")
            raise RuntimeError("Failed to insert topic into MongoDB") from e

def check_mongo_connection():
    username = UP.quote_plus(config.MONGO_USERNAME)
    password = UP.quote_plus(config.MONGO_PASSWORD)
    cluster_url = "cluster0.ocsuk.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    print(username, password, cluster_url)

    if not all([username, password, cluster_url]):
        raise KeyError("MongoDB credentials are not set/loaded correctly.")

    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}"
    print('connection_string: ', connection_string)
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return {"status": "Connection to MongoDB successful!"}
    except Exception as e:
        return {"error": str(e)}
