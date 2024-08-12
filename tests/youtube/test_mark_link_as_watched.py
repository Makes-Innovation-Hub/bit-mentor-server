import pytest
from fastapi.testclient import TestClient
from server.server import app
from model.YouTube_DB import YouTubeService, get_db

client = TestClient(app)


def get_db_override():
    db_service = YouTubeService()
    db_service.add_fake_urls_to_python()  # Add fake URLs from fake1 to fake20
    return db_service


app.dependency_overrides[get_db] = get_db_override


def test_mark_link_as_watched_success():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=fake8"
    }
    # Make a POST request to mark the video URL as watched
    response = client.post("youtube/mark_link_watched", json=request_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User stats updated successfully"}

    # check if the video URL has been added to the user's watched list
    user_data = get_db_override().user_watched_links_collection.find_one({"user_id": request_data["user_id"]})
    assert "https://www.youtube.com/watch?v=fake8" in user_data["watched"]["Python"]["length"]["short"]

    # remove the added URL after the test
    get_db_override().user_watched_links_collection.update_one(
        {"user_id": request_data["user_id"]},
        {"$pull": {"watched.Python.length.short": "https://www.youtube.com/watch?v=fake8"}}
    )
    # check if video URL has been removed
    user_data = get_db_override().user_watched_links_collection.find_one({"user_id": request_data["user_id"]})
    assert "https://www.youtube.com/watch?v=fake8" not in user_data["watched"]["Python"]["length"]["short"]


########################################################################################################################
# MISSING INPUTS
def test_mark_link_as_watched_missing_user_id():
    request_data = {
        "topic": "Python",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=fake1"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 422


def test_mark_link_as_watched_missing_topic():
    request_data = {
        "user_id": "test_user1",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=fake1"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 422


def test_mark_link_as_watched_missing_length():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "video_url": "https://www.youtube.com/watch?v=fake1"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 422


def test_mark_link_as_watched_missing_video_url():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "length": "short"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 422


########################################################################################################################
# INVALID INPUTS
def test_mark_link_as_watched_invalid_length():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "length": "HI",
        "video_url": "https://www.youtube.com/watch?v=fake1"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Video length must be one of 'short', 'medium', or 'long'"}


def test_mark_link_as_watched_invalid_topic():
    request_data = {
        "user_id": "test_user1",
        "topic": "invalid",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=fake1"
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid topic: topic should be in categories"}


def test_mark_link_as_watched_invalid_url():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=invalid"  # URL does not exist in YouTube links
    }

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid video URL: URL does not exist in YouTube links"}


########################################################################################################################
def test_mark_link_as_watched_already_watched():
    request_data = {
        "user_id": "test_user1",
        "topic": "Python",
        "length": "short",
        "video_url": "https://www.youtube.com/watch?v=fake19"
    }
    # The video URL does not exist in the user's watch list, so it should be inserted successfully.

    client.post("youtube/mark_link_watched", json=request_data)

    # return an error because the same URL already exists in the user's watch list.

    response = client.post("youtube/mark_link_watched", json=request_data)

    assert response.status_code == 400
    assert response.json() == {"detail": "This link has already been watched by the user."}

    # remove the added URL after the test
    get_db_override().user_watched_links_collection.update_one(
        {"user_id": request_data["user_id"]},
        {"$pull": {"watched.Python.length.short": "https://www.youtube.com/watch?v=fake19"}}
    )
    # check if video URL has been removed
    user_data = get_db_override().user_watched_links_collection.find_one({"user_id": request_data["user_id"]})
    assert "https://www.youtube.com/watch?v=fake19" not in user_data["watched"]["Python"]["length"]["short"]


########################################################################################################################
# Cleanup function to remove fake URLs from the YouTube links collection
def test_clear_youtube_links_collection():
    db_service = get_db_override()
    fake_urls = [f"https://www.youtube.com/watch?v=fake{i}" for i in range(1, 21)]
    db_service.youtube_links_collection.update_one(
        {"topic": "Python"},
        {"$pull": {"length.short": {"$in": fake_urls}}}
    )