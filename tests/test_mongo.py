import unittest
import os
from setting.config import *
from model.MongoDb import MongoDatabase

mongo_uri = config.MONGO_CLUSTER
database_name = config.DATABASE_NAME
mongo_db = MongoDatabase(mongo_uri, database_name)


class TestMongoConnection(unittest.TestCase):
    def test_check_mongo_connection(self):
        result = mongo_db.check_mongo_connection()
        print(result)
        self.assertIn("status", result)
        self.assertEqual(result["status"], "Connection to MongoDB successful!")


if __name__ == '__main__':
    unittest.main()

