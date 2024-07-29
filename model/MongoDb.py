from pymongo import MongoClient
from pymongo.errors import ConnectionFailure


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
            print(f"MongoDB connection to database '{self.database_name}' successful!")
            return {"message": f"MongoDB connection to database '{self.database_name}' successful!"}
        except ConnectionFailure as e:
            print(f"MongoDB connection failed: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")
