import pytest
import httpx
import random
import string

BASE_URL = "http://127.0.0.1:8000"

@pytest.mark.asyncio
async def test_add_new_topic():
    """Test adding a new topic that doesn't already exist in the database."""
    # Fetch the current topics
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/topics")
        assert response.status_code == 200

        existing_topics = response.json()
        assert isinstance(existing_topics, list)

        # Generate a random topic name that doesn't exist in the database
        while True:
            new_topic = ''.join(random.choices(string.ascii_lowercase, k=10))
            if new_topic not in existing_topics:
                break

        # Add the new topic
        response = await client.post("/add-topic/", json={"topic_name": new_topic})
        assert response.status_code == 200
        assert response.json()["message"] == f"Topic '{new_topic}' successfully inserted."

        # Verify the topic was added by fetching the topics again
        response = await client.get("/topics")
        assert response.status_code == 200
        assert new_topic in response.json()


@pytest.mark.asyncio
async def test_add_existing_topic():
    """Test adding a topic that already exists in the database."""
    # Fetch the current topics
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        response = await client.get("/topics")
        assert response.status_code == 200

        existing_topics = response.json()
        assert isinstance(existing_topics, list)
        assert len(existing_topics) > 0

        # Pick an existing topic to try and add again
        existing_topic = random.choice(existing_topics)

        # Attempt to add the existing topic
        response = await client.post("/add-topic/", json={"topic_name": existing_topic})
        assert response.status_code == 200
        assert response.json()["message"] == f"Topic '{existing_topic}' already exists."


@pytest.mark.asyncio
async def test_add_topic_invalid_request():
    """Test adding a topic with an invalid request or missing fields."""
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        # Attempt to add a topic with a missing field
        response = await client.post("/add-topic/", json={})
        assert response.status_code == 422  # Unprocessable Entity

        # Attempt to add a topic with an invalid JSON structure
        response = await client.post("/add-topic/", content="Invalid data format")
        assert response.status_code == 422  # Unprocessable Entity
