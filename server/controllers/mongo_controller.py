from fastapi import APIRouter, Response, status
from model.MongoDb import MongoDatabase
from pymongo.errors import ConnectionFailure

from dotenv import load_dotenv
import os

from server.utils.logger import app_logger

load_dotenv()

router = APIRouter()

mongo_uri = os.getenv('MONGODB_URI')
database_name = os.getenv('DATABASE_NAME')
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

