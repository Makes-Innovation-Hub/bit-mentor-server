import dotenv
from fastapi import APIRouter, HTTPException
import requests

from setting.config import *

router = APIRouter()

@router.get("/quote")
def root():
    """
    Retrieves a random quote from the API.

    This function sends a GET request to the API endpoint 'https://api.api-ninjas.com/v1/quotes'
    with the 'X-Api-Key' header set to the value of the 'MOTIVATION_API' configuration variable.
    If the response status code is 200 (OK), the function returns the quote in the response JSON.
    Otherwise, it raises an HTTPException with a status code of 400 (Bad Request) and the detail message 'Error'.

    Returns:
        dict: The quote in the response JSON.

    Raises:
        HTTPException: If the response status code is not 200.
    """
    api_url = 'https://api.api-ninjas.com/v1/quotes'
    response = requests.get(api_url, headers={'X-Api-Key': config.MOTIVATION_API})

    if response.status_code == requests.codes.ok:
        return response.json()[0]
    else:
        raise HTTPException(status_code=400, detail="Error")
