from fastapi import APIRouter, Response, status
from server.utils.mongo_utils import check_mongo_connection

router = APIRouter()

@router.get("/check-mongo-connection")
def check_mongo(response: Response):
    try:
        result = check_mongo_connection()
        print(f"Result: {result}")
        response.status_code = status.HTTP_200_OK
        return result
    except KeyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return e
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return e