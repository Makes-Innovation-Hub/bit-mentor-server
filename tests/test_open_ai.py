from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import create_question_and_answer_and_explanation

def test_get_openai_response_contains_keys():
    prompt = create_question_and_answer_and_explanation("python")
    response = get_openai_response(prompt)
    assert isinstance(response, dict)
    assert "question" in response
    assert "answer" in response
    assert "explanation" in response
    assert "fake" not in response