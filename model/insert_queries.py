
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv
from pymongo import MongoClient

import os

load_dotenv()

def insert_question(collection, collection_name, database_name, question_data):
    try:
        result = collection.insert_one(question_data)
        print(f"Data inserted successfully into collection '{collection_name}' in database '{database_name}'.")
        return result.inserted_id
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None




