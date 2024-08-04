from fastapi import APIRouter, Response, status
from model.MongoDb import MongoDatabase
from server.utils.logger import app_logger
from model.MongoDb import MongoDatabase 
from setting.config import *
from pymongo.errors import ConnectionFailure


router = APIRouter()

mongo_uri = config.MONGO_CLUSTER
database_name = config.DATABASE_NAME
mongo_db = MongoDatabase(mongo_uri, database_name)


@router.get("/check-mongo-connection")
def check_mongo(response: Response):
    try:
        result = mongo_db.check_mongo_connection()
        response.status_code = status.HTTP_200_OK
        app_logger.info("Connection to MongoDB successful!")
        return result
    except KeyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        app_logger.error(e)
        return {"error": str(e)}
    except ConnectionFailure as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        app_logger.error({"error": f"MongoDB connection failed: {str(e)}"})
        return {"error": f"MongoDB connection failed: {str(e)}"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        app_logger.error(f"Error connecting to MongoDB: {str(e)}")
        return {"error": str(e)}


    
@router.post("/insert-question")
def insert_question(question_data: dict, response: Response):
    try:
        result = mongo_db.insert_question("questions", question_data)
        response.status_code = status.HTTP_201_CREATED
        return {"inserted_id": str(result)}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}

@router.post("/update-user-stat")
def submit_answer(answer_data: dict, response: Response):
    user_id = answer_data['user_id']
    topic = answer_data['topic']
    difficulty = answer_data['difficulty']
    is_correct = answer_data['is_correct']

    # Increment the appropriate counters
    update_fields = {
        f'stats.topic.{topic}.{difficulty}.questions_answered': 1,
        f'stats.topic.{topic}.{difficulty}.correct_answers': 1 if is_correct else 0
    }

    # Update statistics by topic and difficulty
    mongo_db.update_user_stat( user_id, update_fields)
   

