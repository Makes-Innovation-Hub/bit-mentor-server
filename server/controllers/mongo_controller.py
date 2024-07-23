from fastapi import APIRouter
from model.MongoDb import check_mongo_connection

router = APIRouter()

@router.get("/check-mongo-connection")
def check_mongo():
    return check_mongo_connection()
