import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_generate_question_no_subject():
    """Test the /generate_question endpoint with no subject provided."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"subject": "", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed"


@pytest.mark.asyncio
async def test_generate_question_invalid_subject():
    """Test the /generate_question endpoint with an invalid subject."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"subject": "invalid_subject", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 404
    assert response.json()["detail"] == "Subject 'invalid_subject' not found in available topics."


@pytest.mark.asyncio
async def test_generate_question_valid_subject():
    """Test the /generate_question endpoint with a valid subject."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"subject": "math", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 200

    data = response.json()
    assert "question_text" in data
    assert "options" in data
    assert "details" in data
    assert "correct_answer" in data
    assert "answer" in data


@pytest.mark.asyncio
async def test_generate_question_key_error():
    """Test the /generate_question endpoint to simulate a KeyError."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"subject": "math", "difficulty": "medium", "answers_count": 4})
        # Simulate a KeyError response by manually sending a 500 error response
        assert response.status_code == 500
        assert response.json()["detail"] == "Missing key in response data: 'missing_key'"


@pytest.mark.asyncio
async def test_generate_question_general_error():
    """Test the /generate_question endpoint to simulate a general error."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/", json={"subject": "math", "difficulty": "medium", "answers_count": 4})
        # Simulate a general error response by manually sending a 400 error response
        assert response.status_code == 400
        assert response.json()["detail"] == "An error occurred: Something went wrong"
