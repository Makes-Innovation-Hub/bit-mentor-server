from fastapi import APIRouter, Response,status
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.gen_question_body import GenQuestionBody

router = APIRouter()

@router.post("/generate-question")
def generate_question(body: GenQuestionBody, response :Response):
    try:
        prompt = generate_question_prompt(body.topic,body.difficulty)
        result = get_openai_response(prompt)
        response.status_code = status.HTTP_200_OK
        return result
    except KeyError as e:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return e
    except Exception as e:
        print('e: ', e)
        response.status_code = status.HTTP_400_BAD_REQUEST
        return e
        