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


    def test_check_mongo_connection(self):
        # Test connection to the database
        try:
            result = self.mongo_database.check_mongo_connection()
            self.assertEqual(result, {"message": f"MongoDB connection to database '{self.test_db_name}' successful!"})
        except ConnectionFailure:
            self.fail("MongoDB connection failed")


if __name__ == '__main__':
    unittest.main()

