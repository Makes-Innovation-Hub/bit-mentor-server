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

    def test_insert_question_and_undo(self):
        # Insert a question and verify insertion
        question_data = {"question": "Is insert question works?"}
        collection_name = "Questions"
        self.mongo_database.insert_question(collection_name, question_data)

        # Check if the question is inserted
        inserted_question = self.mongo_database.questions_collection.find_one(question_data)
        self.assertIsNotNone(inserted_question)

        # Clean up by deleting the inserted question
        self.mongo_database.questions_collection.delete_one({"_id": inserted_question["_id"]})

    def test_save_user_answer_and_undo(self):
        # Insert a user answer and verify insertion
        user_answer = {"user_id": 1, "answer": "True"}
        collection_name = "Users"
        self.mongo_database.save_user_answer(collection_name, user_answer)

        # Check if the user answer is inserted
        inserted_answer = self.mongo_database.users_answers_collection.find_one(user_answer)
        self.assertIsNotNone(inserted_answer)

        # Clean up by deleting the inserted user answer
        self.mongo_database.users_answers_collection.delete_one({"_id": inserted_answer["_id"]})

    def test_update_user_stat_and_undo(self):
        # Update a user stat and verify update
        user_id = 1
        update_fields = {"score": 10}
        self.mongo_database.update_user_stat(user_id, update_fields)

        # Check if the user stat is updated
        updated_stat = self.mongo_database.stats_collection.find_one({"user_id": user_id})
        self.assertIsNotNone(updated_stat)
        self.assertEqual(updated_stat["score"], 10)

        # Clean up by deleting the updated user stat
        self.mongo_database.stats_collection.delete_one({"user_id": user_id})

if __name__ == '__main__':
    unittest.main()
