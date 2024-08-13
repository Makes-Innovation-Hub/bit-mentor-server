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
        """
        Generate a question based on the provided subject and difficulty.
    
        This function handles the generation of a question using OpenAI based on the
        `QuestionRequest` provided by the client. Depending on the presence of `answers_count`,
        the function may generate a multiple-choice question or a single-answer question.
    
        Args:
            question (QuestionRequest): The request body containing the question parameters,
                                        including the subject and answers_count.
    
        Returns:
            QuestionResponse: The response containing the generated question, its correct answer,
                              and any additional details.
    
        Raises:
            HTTPException: 
                - 404: If the subject provided in the request is not found in the available topics.
                - 500: If there is a missing key in the response data from OpenAI.
                - 400: For any other general errors that occur during question generation.
        """
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

