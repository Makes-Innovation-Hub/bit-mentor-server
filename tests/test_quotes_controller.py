from fastapi.testclient import TestClient
from server.server import app  # make sure to import your FastAPI app
from setting.config import *
from model.MongoDb import MongoDatabase

client = TestClient(app)
def test_get_quote_success():
    response = client.get("/quote/1")
    assert response.status_code == 200
    response_json = response.json()
    quote = response_json    

    mongo_uri = config.MONGO_CLUSTER
    database_name = config.DATABASE_NAME
    mongo_db = MongoDatabase(mongo_uri, database_name)
    quotes_collection = mongo_db.quotes_collection
    quote_doc = quotes_collection.find_one({'quote': quote})
    if quote_doc:
        result = quotes_collection.update_one(
                {'_id': quote_doc['_id']},
                {'$pull': {'user_ids': 1}}
        )