from fastapi import APIRouter
from server.utils.mongo_utils import check_mongo_connection

router = APIRouter()

@router.get("/check-mongo-connection")
def check_mongo():
    result = check_mongo_connection()
    print(f"Result: {result}")
    return result

