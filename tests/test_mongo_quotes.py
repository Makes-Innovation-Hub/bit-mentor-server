import pytest
import mongomock

# Import the functions to be tested
import model.select_queries as select_queries
import model.insert_queries as insert_queries

@pytest.fixture
def mock_db():
    client = mongomock.MongoClient()
    db = client['test_database']
    yield db

def test_insert_data(mock_db):
    collection = mock_db['test_collection']
    data = {"key": "value"}
    
    inserted_id = insert_queries.insert_data(collection, "test_collection", "test_database", data)
    
    assert inserted_id is not None, "Data insertion failed"
    assert collection.find_one({"_id": inserted_id}) is not None, "Inserted document not found"

def test_insert_quote(mock_db):
    quotes_collection = mock_db['quotes']
    quote = "This is a test quote."
    
    insert_queries.insert_quote(quotes_collection, quote)
    
    found_quote = quotes_collection.find_one({"quote": quote})
    assert found_quote is not None, "Quote insertion failed"
    assert found_quote["quote"] == quote, "Inserted quote does not match"

def test_add_user_to_quote(mock_db):
    quotes_collection = mock_db['quotes']
    quote = {"quote": "This is a test quote.", "user_ids": []}
    quote_id = quotes_collection.insert_one(quote).inserted_id
    
    user_id = "user_123"
    insert_queries.add_user_to_quote(quotes_collection, quote_id, user_id)
    
    updated_quote = quotes_collection.find_one({"_id": quote_id})
    assert user_id in updated_quote["user_ids"], "User ID not added to quote"

def test_get_random_quotes(mock_db):
    quotes_collection = mock_db['quotes']
    
    # Test with empty collection
    quotes = select_queries.get_random_quotes(quotes_collection)
    assert quotes == [], "Expected empty list when collection is empty"
    
    # Insert fewer than 5 quotes
    quotes_collection.insert_many([
        {"quote": "Quote 1", "user_ids": []},
        {"quote": "Quote 2", "user_ids": []},
        {"quote": "Quote 3", "user_ids": []}
    ])
    
    quotes = select_queries.get_random_quotes(quotes_collection)
    assert len(quotes) == 3, "Expected 3 quotes when collection has fewer than 5 quotes"
    
    # Insert more quotes and test again
    quotes_collection.insert_many([
        {"quote": "Quote 4", "user_ids": []},
        {"quote": "Quote 5", "user_ids": []},
        {"quote": "Quote 6", "user_ids": []}
    ])
    
    quotes = select_queries.get_random_quotes(quotes_collection)
    assert len(quotes) == 5, "Expected 5 quotes when collection has more than 5 quotes"

if __name__ == "__main__":
    pytest.main()
