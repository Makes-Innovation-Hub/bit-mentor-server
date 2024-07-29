from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from model.insert_queries import insert_question

# from dotenv import load_dotenv

# load_dotenv()
# mongo_uri = os.getenv('MONGODB_URI')
# database_name = os.getenv('DATABASE_NAME')
# collection_name = os.getenv('COLLECTION_NAME')


class MongoDatabase:
    def __init__(self, uri, database_name):
        self.uri = uri
        self.client = MongoClient(uri)
        self.database_name = database_name
        self.db = self.client[database_name]
        self.questions_collection = self.db["Questions"]
        self.users_collection = None
        self.topics_collection = None


    def insert_question(self,collection_name,question_data):
        if not self.client:
            self.check_mongo_connection(self.uri,self.database_name)
        try:
            questions_collection = self.questions_collection
            return insert_question(questions_collection,collection_name,self.database_name,question_data)
        except Exception as e:
            print(f"An error occurred while inserting data: {e}")
            raise Exception(f"An error occurred while inserting data: {e}")



    def check_mongo_connection(self):
            try:
                self.client.admin.command('ismaster')
                print(f"MongoDB connection to database '{self.database_name}' successful!")
                return {"message": f"MongoDB connection to database '{self.database_name}' successful!"}
            except ConnectionFailure as e:
                print(f"MongoDB connection failed: {e}")
            except Exception as e:
                print(f"An error occurred: {e}")



