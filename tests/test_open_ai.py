from server.utils.open_ai import get_openai_response
from server.utils.ai_prompt import generate_question_prompt
from fastapi.testclient import TestClient
from server.server import app


def test_get_openai_response_contains_keys():
    prompt = generate_question_prompt("python")
    response = get_openai_response(prompt)
    assert isinstance(response, dict)
    assert "question" in response
    assert "answer" in response
    assert "explanation" in response
    assert "fake" not in response


client = TestClient(app)


def test_generate_question():
    response = client.post("/generate-question", json={"topic": "python"}, )
    assert response.status_code == 200
    result = response.json()
    assert "question" in result
    assert "answer" in result
    assert "explanation" in result
    assert len(result["question"]) <= 100
    assert "python" in result["question"].lower()
