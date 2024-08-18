from fastapi.testclient import TestClient
from server.server import app  # make sure to import your FastAPI app
from setting.config import *
from model.MongoDb import MongoDatabase

client = TestClient(app)
def test_get_quote_success():
    """
    Tests the successful retrieval of a quote from the API.
    
    This function sends a GET request to the '/quote/1' endpoint and asserts that the response status code is 200.
    
    """
    response = client.get("/quote/1")
    assert response.status_code == 200
    response_json = response.json()

    mongo_uri = config.MONGO_CLUSTER
    database_name = config.DATABASE_NAME
    mongo_db = MongoDatabase(mongo_uri, database_name)
    quotes_collection = mongo_db.quotes_collection
    quote_doc = quotes_collection.find_one({'quote': response_json})
    if quote_doc:
        result = quotes_collection.update_one(
                {'_id': quote_doc['_id']},
                {'$pull': {'user_ids': 1}}
        )
