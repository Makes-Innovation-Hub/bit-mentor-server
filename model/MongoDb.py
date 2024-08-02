from pymongo import MongoClient
from pymongo.errors import ConnectionFailure

from server.utils.logger import app_logger


class MongoDatabase:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database_name = database_name
        self.db = self.client[database_name]
        self.questions_collection = self.db["Questions"]
        self.users_collection = None
        self.topics_collection = None

    def check_mongo_connection(self):
        try:
            self.client.admin.command('ismaster')
            app_logger.info(f"MongoDB connection to database '{self.database_name}' successful!")
            return {"message": f"MongoDB connection to database '{self.database_name}' successful!"}
        except ConnectionFailure as e:
            app_logger.error(f"MongoDB connection failed: {e}")
        except Exception as e:
            app_logger.error(f"An error occurred: {e}")
            app_logger.error(f"An error occurred: {e}")
