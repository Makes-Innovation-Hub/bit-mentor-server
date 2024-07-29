from fastapi import APIRouter, Response, status
from model.MongoDb import MongoDatabase 
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv
import os

load_dotenv()

router = APIRouter()

# Initialize MongoDatabase instance
mongo_uri = os.getenv('MONGO_CLUSTER_URL')
database_name = os.getenv('DATABASE_NAME')
mongo_db = MongoDatabase(mongo_uri, database_name)
# questions_collection = os.

@router.get("/check-mongo-connection")
def check_mongo(response: Response):
    try:
        result = mongo_db.check_mongo_connection()
        response.status_code = status.HTTP_200_OK
        return result
    except KeyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}
    except ConnectionFailure as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": f"MongoDB connection failed: {str(e)}"}
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
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
    

 