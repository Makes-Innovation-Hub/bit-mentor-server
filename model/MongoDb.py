from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from server.utils.logger import app_logger
from model.insert_queries import *
import urllib.parse as UP
from setting.config import *
class MongoDatabase:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database_name = database_name
        self.db = self.client[database_name]
        self.questions_collection = self.db["Questions"]
        self.users_answers_collection = self.db["Users"]
        self.stats_collection = self.db["stats"]
        self.quotes_collection = self.db["quotes"]

    def insert_question(self,collection_name,question_data):
        if not self.client:
            self.check_mongo_connection(self.uri,self.database_name)
        try:
            questions_collection = self.questions_collection
            return insert_data(questions_collection,collection_name,self.database_name,question_data)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
            raise Exception(f"An error occurred while inserting data: {e}")
    
    def update_user_stat(self, user_id, update_fields):
        self.stats_collection.update_one(
        {'user_id': user_id},
        {'$inc': update_fields},
        upsert=True
    )

    def save_user_answer(self,collection_name, user_answer):
        if not self.client:
            self.check_mongo_connection(self.uri,self.database_name)
        try:
            users_answers_collection = self.users_answers_collection
            return insert_data(users_answers_collection,collection_name,self.database_name,user_answer)
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

