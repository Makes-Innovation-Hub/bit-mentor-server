from pymongo.errors import ConnectionFailure
from server.utils.logger import app_logger
def insert_data(collection, collection_name, database_name, data):
    try:
        result = collection.insert_one(data)
        print(f"Data inserted successfully into collection '{collection_name}' in database '{database_name}'.")
        return result.inserted_id
    except ConnectionFailure as e:
        print(f"MongoDB connection failed: {e}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    

def insert_quote(quotes_collection, quote):
    try:
        quotes_collection.insert_one({'quote': quote, 'user_ids': []})
        app_logger.info(f"Quote inserted: {quote}")
    except Exception as e:
        app_logger.error(f"Failed to insert quote: {e}")

def add_user_to_quote(quotes_collection, quote_id, user_id):
    try:
        quotes_collection.update_one(
            {'_id': quote_id},
            {'$addToSet': {'user_ids': user_id}}
        )
        app_logger.info(f"User {user_id} added to quote {quote_id}")
    except Exception as e:
        app_logger.error(f"Failed to add user to quote: {e}")





