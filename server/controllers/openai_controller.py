from fastapi import APIRouter, HTTPException
from server.utils.open_ai import get_question_and_answer_and_explanation

router = APIRouter()

@router.get("/generate-question/{topic}")
def get_generated_question(topic: str):
    result = get_question_and_answer_and_explanation(topic)
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    return result
