from fastapi import APIRouter, Response, status

from server.utils.logger import RequestIdFilter
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.gen_question_body import GenQuestionBody
from server.utils.logger import app_logger, generate_request_id

router = APIRouter()


@router.post("/generate-question")
async def generate_question(body: GenQuestionBody, response: Response):
    app_logger.info(f"Received request to generate question with body: {body.dict()}")
    try:
        prompt = generate_question_prompt(body.topic, body.difficulty)
        app_logger.info(f"Generated prompt: {prompt}")

        result = get_openai_response(prompt)
        response.status_code = status.HTTP_200_OK
        app_logger.info(f"Successfully generated response: {result}")

        return result

    except KeyError as e:
        app_logger.error(f"KeyError occurred: {str(e)}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {"error": str(e)}

    except Exception as e:
        app_logger.error(f"An unexpected error occurred: {str(e)}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"error": str(e)}
