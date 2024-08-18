from fastapi import APIRouter, Response, status, HTTPException, Body
from model.MongoDb import MongoDatabase
from server.utils.logger import app_logger
from model.MongoDb import MongoDatabase 
from setting.config import *
from pymongo.errors import ConnectionFailure, PyMongoError
from model.MongoDb import check_mongo_connection



router = APIRouter()

mongo_uri = config.MONGO_CLUSTER
database_name = config.DATABASE_NAME
mongo_db = MongoDatabase(mongo_uri, database_name)


@router.get("/topics", response_model=list[str], tags=["topics"])
async def get_topics():
    """
    Retrieve the list of available topics for questions.
    
    Returns:
        list[str]: A list of topic names.
    
    Raises:
        HTTPException: If there is an error retrieving the topics.
    """
    try:
        topics = mongo_db.load_topics_from_mongo()
        return topics
    except RuntimeError as e:
        app_logger.error(f"Failed to retrieve topics: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving topics"
        )


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
    score = answer_data['score']
    is_correct = False
    if score > 0:
        is_correct = True

    # Increment the appropriate counters
    update_fields = {
        f'stats.topic.{topic}.{difficulty}.questions_answered': 1,
        f'stats.topic.{topic}.{difficulty}.correct_answers': 1 if is_correct else 0,
        f'stats.topic.{topic}.{difficulty}.total_score': score
    }

    # Update statistics by topic and difficulty
    mongo_db.update_user_stat( user_id, update_fields)


@router.post("/add-topic/")
async def add_topic(topic_name: str = Body(..., embed=True)):
    """
    Add a new topic to the MongoDB allowed_topics collection.

    Args:
        topic_name (str): The name of the topic to add.

    Returns:
        dict: A message indicating the result of the operation.

    Raises:
        HTTPException: If there is an error inserting the topic.
    """
    try:
        result = mongo_db.insert_new_topic(topic_name)
        return result
    except RuntimeError as e:
        app_logger.error(f"Failed to add topic '{topic_name}': {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))