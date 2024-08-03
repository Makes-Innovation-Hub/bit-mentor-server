from fastapi import APIRouter, Response,status,HTTPException
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.gen_question_body import *
import requests
import os
from dotenv import load_dotenv

load_dotenv()
router = APIRouter()
from pydantic import BaseModel



@router.post("/generate-question")
def generate_question(body: GenQuestionBody, response :Response):
    try:
        prompt = generate_question_prompt(body.topic,body.difficulty)
        result = get_openai_response(prompt)
        question = result["question"]
        answer = result["answer"]
        explanation = result["explanation"]
        response.status_code = status.HTTP_200_OK
        return OpenQuestionResponse(
            question=question,
            answer=answer,
            explanation=explanation
        )
    except KeyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return e
    except Exception as e:
        print('e: ', e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return e
        

@router.post("/check_answer")
def check_user_answer(request:AnswerCheckRequest):
    openai_key = os.getenv("OPENAI_KEY")
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
        "max_tokens": 10
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



