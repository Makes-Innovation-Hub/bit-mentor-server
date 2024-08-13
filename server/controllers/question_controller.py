from fastapi import HTTPException, APIRouter

from server.controllers.mongo_controller import mongo_db
from server.utils.ai_prompt import generate_question_with_multiple_options
from server.utils.logger import app_logger
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.question_models import QuestionRequest, QuestionResponse
from server.utils.question_processing import process_question_request

router = APIRouter()


@router.post("/", response_model=QuestionResponse)
async def generate_question(question: QuestionRequest):
    try:
        if question.subject in mongo_db.load_topics_from_mongo():
            with_answers = True if question.answers_count and question.answers_count > 0 else False
            if with_answers:
                prompt = generate_question_with_multiple_options(question)
            else:
                prompt = generate_question_prompt(question)
            app_logger.info(f"Generated prompt: {prompt}")
            result = get_openai_response(prompt)

            question_response = process_question_request(result,with_answers)

            return question_response
        else:
            app_logger.warning(f"Subject '{question.subject}' not found in topics.")
            raise HTTPException(status_code=404, detail=f"Subject '{question.subject}' not found in available topics.")
    except KeyError as e:
        app_logger.error(f"Missing key in response data: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Missing key in response data: {str(e)}")
    except Exception as e:
        app_logger.error(f"An error occurred while generating question: {str(e)}")
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

