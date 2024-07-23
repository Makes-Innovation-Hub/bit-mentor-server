import unittest
from model.MongoDb import check_mongo_connection


class TestMongoConnection(unittest.TestCase):
    def test_check_mongo_connection(self):
        result = check_mongo_connection()
        self.assertIn("status", result)
        self.assertEqual(result["status"], "Connection to MongoDB successful!")

if __name__ == '__main__':
    unittest.main()
