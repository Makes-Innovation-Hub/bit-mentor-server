import unittest
from pymongo.errors import ConnectionFailure
from model.MongoDb import MongoDatabase 
from setting.config import *

class TestMongoDatabase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Connect to the test MongoDB instance
        cls.test_uri = config.MONGO_CLUSTER 
        cls.test_db_name = config.DATABASE_NAME
        cls.mongo_database = MongoDatabase(cls.test_uri, cls.test_db_name)

    def test_load_topics_success(self):
        # Arrange: Insert sample topics into the collection
        self.mongo_database.topics.delete_many({})
        self.mongo_database.topics.insert_many([
            {"name": "python"},
            {"name": "algorithms"}
        ])

        # Act: Call the method to load topics
        topics = self.mongo_database.load_topics_from_mongo()

        # Assert: Verify the topics match the expected result
        self.assertEqual(topics, ["python", "algorithms"])
        self.mongo_database.topics.delete_many({})

    def test_load_topics_empty(self):
        self.mongo_database.topics.delete_many({})
        # Act: Call the method to load topics from an empty collection
        topics = self.mongo_database.load_topics_from_mongo()

        # Assert: Verify that an empty list is returned
        self.assertEqual(topics, [])

if __name__ == "__main__":
    unittest.main()