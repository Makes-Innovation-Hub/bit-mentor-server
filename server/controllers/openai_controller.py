from server.utils.logger import RequestIdFilter
from data_types.question_models import GenQuestionBody
from server.utils.logger import app_logger, generate_request_id
from fastapi import APIRouter, Response,status,HTTPException, Depends
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.question_models import *
import requests
from setting.config import *
import re
from server.middlewares.auth_middlewares import check_token
router = APIRouter()



@router.post("/check_answer")
def check_user_answer(request: AnswerCheckRequest, is_telegram_user = Depends(check_token)):
    if not is_telegram_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    openai_key = config.OPENAI_KEY
    if not openai_key:
        raise HTTPException(status_code=500, detail="OpenAI API key is not loaded")

    prompt = (
        f"Question: {request.question}\n"
        f"User Answer: {request.user_answer}\n"
        f"Rate the accuracy of the user's answer on a scale of 0 to 10, "
        f"where 0 means totally wrong and 10 means very accurate. "
        f"Provide only the numerical score."
    )
    
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
        
        answer_score_str = result["choices"][0]["message"]["content"].strip()

        # Use regex to extract the first integer from the response
        match = re.search(r'\b\d+\b', answer_score_str)
        print(match)
        if match:
            answer_score = int(match.group())
            if not 0 <= answer_score <= 10:
                raise ValueError("Score out of range")
        else:
            raise ValueError("No valid score found")

        return {"score": answer_score}
    
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Failed to process the request with OpenAI API")
    except (ValueError, KeyError):
        raise HTTPException(status_code=500, detail="Unexpected response format from OpenAI API")


