import os
from pymongo import MongoClient
from dotenv import load_dotenv

from setting.config import *

load_dotenv()


def check_mongo_connection():
    username = config.MONGO_USERNAME
    password = config.MONGO_PASSWORD
    cluster_url = config.MONGO_CLUSTER
    print(username, password, cluster_url)

    if not all([username, password, cluster_url]):
        return {"error": "MongoDB credentials are not set."}

    connection_string = f"mongodb+srv://{username}:{password}@{cluster_url}"
    try:
        client = MongoClient(connection_string)
        client.admin.command('ping')
        return {"status": "Connection to MongoDB successful!"}
    except Exception as e:
        return {"error": str(e)}
