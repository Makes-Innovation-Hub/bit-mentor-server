from fastapi import APIRouter, Depends, HTTPException, status
from server.utils.llm_utils import generate_question

router = APIRouter()

@router.get("/generate-question/{topic}")
def get_generated_question(topic: str):
    result = generate_question(topic)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
