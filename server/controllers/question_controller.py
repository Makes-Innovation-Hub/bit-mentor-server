from fastapi import APIRouter, HTTPException
from data_types.gen_question_body import QuestionRequest, QuestionResponse
from server.utils.ai_prompt import create_question_with_multiple_options
from server.utils.open_ai import get_openai_response

router = APIRouter()


@router.post("/question", response_model=QuestionResponse)
async def generate_question(request: QuestionRequest):
    try:

        prompt = create_question_with_multiple_options(request)
        response = get_openai_response(prompt)

        # Extract the response data
        question_text = response["question_text"]
        options = response["options"]
        details = response["details"]
        correct_answer = response["correct_answer"]

        return QuestionResponse(
            question_text=question_text,
            options=options,
            details=details,
            correct_answer=correct_answer
        )
    except KeyError as e:
        raise HTTPException(status_code=500, detail=f"Missing key in response data: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")