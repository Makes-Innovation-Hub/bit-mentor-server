from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt, generate_question_with_multiple_options
from fastapi.testclient import TestClient
from server.server import app
from data_types.question_models import QuestionRequest


def test_get_openai_response_contains_keys():
    question = QuestionRequest(subject="python", difficulty="easy", answers_count=4)

    prompt = generate_question_with_multiple_options(question)

    response = get_openai_response(prompt)
    assert isinstance(response, dict)
    assert "question_text" in response
    assert "correct_answer" in response
    assert "options" in response
    assert "details" in response
    assert "fake" not in response


def test_get_openai_response_contains_keys_withoutAnswers():
    question = QuestionRequest(subject="python", difficulty="easy", answers_count=0)

    prompt = generate_question_prompt(question)

    response = get_openai_response(prompt)

    assert isinstance(response, dict)
    assert "question_text" in response
    assert "answer" in response
    assert "details" in response
    assert "fake" not in response


client = TestClient(app)
