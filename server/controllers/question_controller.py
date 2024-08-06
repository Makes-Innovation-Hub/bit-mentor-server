from fastapi import HTTPException, APIRouter
from server.utils.ai_prompt import generate_question_with_multiple_options
from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from data_types.question_models import QuestionRequest, QuestionResponse
from server.utils.question_processing import process_question_request

router = APIRouter()


@router.post("/", response_model=QuestionResponse)
async def generate_question(question: QuestionRequest):
    try:
        with_answers = True if question.answers_count and question.answers_count > 0 else False
        if with_answers:
            prompt = generate_question_with_multiple_options(question)
        else:
            prompt = generate_question_prompt(question)

        # Get response data from OpenAI
        result = get_openai_response(prompt)
        # Extract the response data
        question_response = process_question_request(result,with_answers)
        return question_response

    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key in response data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred: {str(e)}")

