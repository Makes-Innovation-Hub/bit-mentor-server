from fastapi import APIRouter, HTTPException
import requests
import model.select_queries as select_queries
import model.insert_queries as insert_queries
from setting.config import *
from model.MongoDb import MongoDatabase
from server.utils.logger import app_logger

router = APIRouter()

mongo_uri = config.MONGO_CLUSTER
database_name = config.DATABASE_NAME
mongo_db = MongoDatabase(mongo_uri, database_name)
quotes_collection = mongo_db.quotes_collection

@router.get("/quote/{user_id}")
def get_quote(user_id: int):
    """
    Retrieves a random quote from the API.
    This function sends a GET request to the API endpoint 'https://api.api-ninjas.com/v1/quotes'
    with the 'X-Api-Key' header set to the value of the 'MOTIVATION_API' configuration variable.
    If the response status code is 200 (OK), the function returns the quote in the response JSON.
    Otherwise, it raises an HTTPException with a status code of 400 (Bad Request) and the detail message 'Error'.
    Returns:
        dict: The quote in the response JSON.
    Raises:
        HTTPException: If the response status code is not 200.
    """
    quotes = select_queries.get_random_quotes(quotes_collection)
    for quote in quotes:
        if user_id not in quote['user_ids']:
            insert_queries.add_user_to_quote(quotes_collection, quote['_id'], user_id)
            return quote['quote']

    api_url = 'https://api.api-ninjas.com/v1/quotes'
    response = requests.get(api_url, headers={'X-Api-Key': config.MOTIVATION_API})
    
    if response.status_code == requests.codes.ok:
        new_quote = response.json()[0]
        insert_queries.insert_quote(quotes_collection, new_quote)
        quote_doc = quotes_collection.find_one({'quote': new_quote})
        if quote_doc:
            insert_queries.add_user_to_quote(quotes_collection, quote_doc['_id'], user_id)
            return new_quote

    else:
        app_logger.warning("Failed to retrieve a new quote from the API")
        raise HTTPException(status_code=400, detail="Error")
