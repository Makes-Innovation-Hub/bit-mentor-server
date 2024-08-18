from server.utils.logger import RequestIdFilter
from data_types.question_models import GenQuestionBody
from server.utils.logger import app_logger, generate_request_id
from fastapi import APIRouter, Response,status,HTTPException
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.question_models import *
import requests
from setting.config import *
router = APIRouter()



@router.post("/check_answer")
def check_user_answer(request:AnswerCheckRequest):
    openai_key = config.OPENAI_KEY
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is not loaded")

    prompt = f"Question: {request.question}\nUser Answer: {request.user_answer}\nIs the user answer correct? Yes or No."
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_key}"
    }
    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
    }
    try:
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        if "choices" not in result or not result["choices"]:
            raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API")
        answer_check = result["choices"][0]["message"]["content"].strip()
        return {"is_correct": answer_check.lower() == "yes."}
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail="Failed to process the request with OpenAI API")
    except KeyError as e:
        raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API")




