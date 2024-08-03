from pymongo.errors import ConnectionFailure

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
    






