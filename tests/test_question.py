from fastapi.testclient import TestClient
from server.server import app
from constants import QUESTION_URL

client = TestClient(app)


def test_generate_question_with_answers_success():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": 4
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": True})
    assert response.status_code == 200
    response_json = response.json()
    assert "question_text" in response_json
    assert "options" in response_json
    assert "details" in response_json
    assert "correct_answer" in response_json

    assert isinstance(response_json["question_text"], str)
    assert len(response_json["question_text"]) > 0
    assert len(response_json["question_text"]) < 100

    assert isinstance(response_json["options"], list)
    assert len(response_json["options"]) == 4
    for option in response_json["options"]:
        assert isinstance(option, str), "Each option should be a string"

    assert isinstance(response_json["details"], list)
    assert len(response_json["details"]) == 4
    for detail in response_json["details"]:
        assert isinstance(detail, str), "Each detail should be a string"

    assert isinstance(response_json["correct_answer"], int)
    assert 0 <= response_json["correct_answer"] < 4


def test_generate_question_wrong_request_with_answers():
    request_payload = {
        "a": "python",
        "b": "easy",
        "c": 4
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": True})
    assert response.status_code == 422


def test_generate_question_missing_field_with_answers():
    request_payload = {
        "subject": "python",
        "difficulty": "easy"
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": True})
    assert response.status_code == 422


def test_generate_question_invalid_data_type_with_answers():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": "four"  # not int
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": True})
    assert response.status_code == 422


def test_generate_question_with_options_true_and_count_zero():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": 0
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": True})
    assert response.status_code == 400
    assert "An error occurred:" in response.json()["detail"]
    assert "If 'with_options' is True, 'answers_count' must be greater than 0." in response.json()["detail"]


def test_generate_question_with_options_false_and_count_greater_than_zero():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": 4
    }

    response = client.post(QUESTION_URL, json=request_payload, params={"with_options": False})
    assert response.status_code == 400
    assert "An error occurred:" in response.json()["detail"]
    assert "If 'with_options' is False, 'answers_count' must be 0." in response.json()["detail"]
