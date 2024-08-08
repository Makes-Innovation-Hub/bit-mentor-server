import pytest
from fastapi.testclient import TestClient
from server.server import app
from model.YouTube_DB import YouTubeService, get_db
from constants import CATEGORIES

client = TestClient(app)


def get_db_override():
    db_service = YouTubeService()
    db_service.add_fake_urls_to_python()  # Add fake URLs from fake1 to fake20
    return db_service


app.dependency_overrides[get_db] = get_db_override


def test_initialize_collections():
    db_service = get_db_override()

    for category in CATEGORIES:
        db_service.youtube_links_collection.delete_many({"topic": category})
    db_service.initialize_collections()

    for category in CATEGORIES:
        entry = db_service.youtube_links_collection.find_one({"topic": category})
        assert entry is not None
        assert "length" in entry
        assert "short" in entry["length"]
        assert "medium" in entry["length"]
        assert "long" in entry["length"]
        assert entry["length"]["short"] == []
        assert entry["length"]["medium"] == []
        assert entry["length"]["long"] == []


def test_initialize_user():
    db_service = get_db_override()
    test_user_id = "test_user1"

    db_service.user_watched_links_collection.delete_many({"user_id": test_user_id})

    initialized_data = db_service.initialize_user(test_user_id)

    assert initialized_data["user_id"] == test_user_id
    assert "watched" in initialized_data

    for category in CATEGORIES:
        assert category in initialized_data["watched"]
        assert "length" in initialized_data["watched"][category]
        assert "short" in initialized_data["watched"][category]["length"]
        assert "medium" in initialized_data["watched"][category]["length"]
        assert "long" in initialized_data["watched"][category]["length"]

        assert initialized_data["watched"][category]["length"]["short"] == []
        assert initialized_data["watched"][category]["length"]["medium"] == []
        assert initialized_data["watched"][category]["length"]["long"] == []


def test_find_youtube_links_by_topic_and_length():
    db_service = get_db_override()
    links = db_service.find_youtube_links_by_topic_and_length("Python", "short")
    assert len(links) == 20
    links = db_service.find_youtube_links_by_topic_and_length("Python", "long")
    assert len(links) == 0


def test_link_exists_in_user_watched():
    db = get_db_override()
    initialized_data = db.initialize_user("test_user1")

    db.user_watched_links_collection.update_one(
        {"user_id": ""},
        {"$pull": {"watched.Python.length.short": "https://www.youtube.com/watch?v=fake1"}}
    )
    # check if video URL has been removed
    user_data = get_db_override().user_watched_links_collection.find_one({"user_id": "test_user1"})
    assert "https://www.youtube.com/watch?v=fake1" not in user_data["watched"]["Python"]["length"]["short"]

    flag = db.link_exists_in_user_watched("test_user1", "Python", "short", "https://www.youtube.com/watch?v=fake1")
    assert flag == False


def test_update_user_stats():
    user_id = "test_user1"
    topic = "Python"
    length = "short"
    video_url = "https://www.youtube.com/watch?v=1"

    db_service = get_db_override()

    assert not db_service.link_exists_in_user_watched(user_id, topic, length, video_url)

    update_result = db_service.update_user_stats(user_id, topic, length, video_url)
    assert update_result is True

    assert db_service.link_exists_in_user_watched(user_id, topic, length, video_url)

    db_service.user_watched_links_collection.update_one(
        {"user_id": user_id},
        {"$pull": {f"watched.{topic}.length.{length}": video_url}}
    )
    assert not db_service.link_exists_in_user_watched(user_id, topic, length, video_url)


def test_clear_youtube_links_collection():
    db_service = get_db_override()
    fake_urls = [f"https://www.youtube.com/watch?v=fake{i}" for i in range(1, 21)]
    db_service.youtube_links_collection.update_one(
        {"topic": "Python"},
        {"$pull": {"length.short": {"$in": fake_urls}}}
    )
