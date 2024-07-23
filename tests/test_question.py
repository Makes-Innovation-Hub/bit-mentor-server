import pytest
import pytest
import os

from fastapi.testclient import TestClient
from server.server import app
from unittest.mock import patch

client = TestClient(app)


def test_generate_question_success():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": 4
    }

    response = client.post("questions/question", json=request_payload)
    assert response.status_code == 200
    response_json = response.json()
    assert "question_text" in response_json
    assert "options" in response_json
    assert "details" in response_json
    assert "correct_answer" in response_json


def test_generate_question_wrong_request():
    request_payload = {
        "a": "python",
        "b": "easy",
        "c": 4
    }

    response = client.post("questions/question", json=request_payload)
    assert response.status_code == 422


def test_generate_question_missing_field():
    request_payload = {
        "subject": "python",
        "difficulty": "easy"
    }

    response = client.post("questions/question", json=request_payload)
    assert response.status_code == 422


def test_generate_question_invalid_data_type():
    request_payload = {
        "subject": "python",
        "difficulty": "easy",
        "answers_count": "four"  # not int
    }

    response = client.post("questions/question", json=request_payload)
    assert response.status_code == 422


