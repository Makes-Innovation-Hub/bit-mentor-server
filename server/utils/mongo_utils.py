import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def check_mongo_connection():
    username = os.getenv("MONGO_USERNAME")
    password = os.getenv("MONGO_PASSWORD")
    cluster_url = os.getenv("MONGO_CLUSTER_URL")

    if not all([username, password, cluster_url]):
        raise KeyError("MongoDB credentials are not set/loaded correctly.")

    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}"
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return {"status": "Connection to MongoDB successful!"}
    except Exception as e:
        return {"error": str(e)}

