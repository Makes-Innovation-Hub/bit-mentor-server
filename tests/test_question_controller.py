import pytest
import httpx

BASE_URL = "http://127.0.0.1:8000"


@pytest.mark.asyncio
async def test_generate_question_no_subject():
    """Test the /generate_question endpoint with no subject provided."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/questions/", json={"subject": "", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 404
    assert response.json()["detail"] == "Subject '' not found in available topics."


@pytest.mark.asyncio
async def test_generate_question_invalid_subject():
    """Test the /generate_question endpoint with an invalid subject."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/questions/",
                                     json={"subject": "invalid_subject", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 404
    assert response.json()["detail"] == "Subject 'invalid_subject' not found in available topics."

#
@pytest.mark.asyncio
async def test_generate_question_invalid_difficulty():
    """Test the /generate_question endpoint with an invalid subject."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/questions/", json={"subject": "sql", "difficulty": "invalid", "answers_count": 4})
    assert response.status_code == 404
    assert response.json()["detail"] == "question difficulty must be one of 'easy', 'medium', or 'hard', or 'none' "


@pytest.mark.asyncio
async def test_generate_question_valid_subject():
    """Test the /generate_question endpoint with a valid subject."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.post("/questions/", json={"subject": "sql", "difficulty": "medium", "answers_count": 4})
    assert response.status_code == 200

    data = response.json()
    assert "question_text" in data
    assert "options" in data
    assert "details" in data
    assert "correct_answer" in data
    assert "answer" in data
