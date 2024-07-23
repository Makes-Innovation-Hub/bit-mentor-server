import json
from unittest.mock import patch, Mock

from server.utils.open_ai import get_openai_response, create_question_and_answer_and_explanation, \
    get_question_and_answer_and_explanation


@patch('server.utils.open_ai.client.chat.completions.create')
def test_get_openai_response_success(mock_create):
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json.dumps({
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern web framework for building APIs with Python.",
        "explanation": "FastAPI is designed for high performance and productivity, leveraging Python's type hints to improve code readability and reduce bugs."
    })
    mock_create.return_value = mock_response

    prompt = "What is FastAPI?"
    response, error = get_openai_response(prompt)
    assert not error
    assert response["question"] == "What is FastAPI?"
    assert response["answer"] == "FastAPI is a modern web framework for building APIs with Python."
    assert response[
               "explanation"] == "FastAPI is designed for high performance and productivity, leveraging Python's type hints to improve code readability and reduce bugs."


@patch('server.utils.open_ai.client.chat.completions.create')
def test_get_openai_response_failure(mock_create):
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Some non-JSON response"
    mock_create.return_value = mock_response

    prompt = "What is FastAPI?"
    response, error = get_openai_response(prompt)
    assert not error
    assert response == "Some non-JSON response"


@patch('server.utils.open_ai.client.chat.completions.create', side_effect=Exception("Test exception"))
def test_get_openai_response_exception(mock_create):
    prompt = "What is FastAPI?"
    response, error = get_openai_response(prompt)
    assert error
    assert "An error occurred: Test exception" in response


def test_create_question_and_answer_and_explanation():
    subject = "Python programming"
    result = create_question_and_answer_and_explanation(subject)
    expected_result = ("Give me a question, answer, and explanation on Python programming. Return them in a dictionary "
                       "format with the keys 'question' 'answer' 'explanation'. Limit the question length to 100 chars.")
    assert result == expected_result


@patch('server.utils.open_ai.client.chat.completions.create')
def test_get_question_and_answer_and_explanation(mock_create):
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = json.dumps({
        "question": "What is FastAPI?",
        "answer": "FastAPI is a modern web framework for building APIs with Python.",
        "explanation": "FastAPI is designed for high performance and productivity, leveraging Python's type hints to improve code readability and reduce bugs."
    })
    mock_create.return_value = mock_response

    prompt = "Python programming"
    response, error = get_question_and_answer_and_explanation(prompt)
    assert not error
    assert response["question"] == "What is FastAPI?"
    assert response["answer"] == "FastAPI is a modern web framework for building APIs with Python."
    assert response[
               "explanation"] == "FastAPI is designed for high performance and productivity, leveraging Python's type hints to improve code readability and reduce bugs."
