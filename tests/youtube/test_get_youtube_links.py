from unittest.mock import patch

from starlette.testclient import TestClient
from server.server import app

client = TestClient(app)


def test_invalid_topic():
    request_data = {
        "topic": "unknown_topic",
        "length": "medium",
        "user_id": "user1"
    }
    response = client.post("/youtube/", json=request_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid topic: topic should be in categories"}


def test_invalid_length():
    request_data = {
        "topic": "SQL",
        "length": "invalid",
        "user_id": "user1"
    }
    response = client.post("/youtube/", json=request_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Video length must be one of 'short', 'medium', or 'long'"}


def test_valid_topic_and_length_no_available_links():
    request_data = {
        "topic": "Python",
        "length": "medium",
        "user_id": "user1"
    }

    with patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_by_topic_and_length", return_value=([],[])), \
            patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_user_by_topic_and_length",
                  return_value=[]), \
            patch("server.utils.youtube.YouTubeService.connect_to_youtube_api", return_value=True), \
            patch("server.utils.youtube.YouTubeService.fetch_youtube_links", return_value=(["link1", "link2", "link3"], ["title1", "title2", "title3"])):

        response = client.post("/youtube/", json=request_data)
        assert response.status_code == 404
        assert response.json() == {"detail": "No videos found for the given topic and length"}


def test_valid_topic_and_length_available_links2():
    request_data = {
        "topic": "Python",
        "length": "medium",
        "user_id": "user1"
    }
    user_links=["link1"]
    youtube_links=["link1", "link2", "link3","link4","link5","link6"]
    youtube_titles=["title1", "title2", "title3","title4","title5","title6"]
    with patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_by_topic_and_length", return_value=(youtube_links,youtube_titles)), \
            patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_user_by_topic_and_length",
                  return_value=user_links), \
            patch("server.utils.youtube.YouTubeService.connect_to_youtube_api", return_value=True), \
            patch("server.utils.youtube.YouTubeService.fetch_youtube_links", return_value=([],[])):

        response = client.post("/youtube/", json=request_data)
        assert response.status_code == 200
        for i in response.json()[0]:
            assert i in youtube_links
        assert len(response.json()) == 2
        assert len(response.json()[0]) == 5


def test_valid_topic_and_length_no_available_links3():
    request_data = {
        "topic": "Python",
        "length": "medium",
        "user_id": "user1"
    }
    user_links=["link1", "link2", "link3"]
    youtube_links=["link1", "link2", "link3","link4","link5","link6"]
    youtube_titles = ["title1", "title2", "title3", "title4", "title5", "title6"]
    with patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_by_topic_and_length", return_value=(youtube_links,youtube_titles)), \
            patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_user_by_topic_and_length",
                  return_value=user_links), \
            patch("server.utils.youtube.YouTubeService.connect_to_youtube_api", return_value=True), \
            patch("server.utils.youtube.YouTubeService.fetch_youtube_links", return_value=(["link7","link8"],["title7","title8"])):

        response = client.post("/youtube/", json=request_data)
        assert response.status_code == 200
        assert "link7" and "link8" in response.json()[0]
        assert "link4" and "link5" and "link6" in response.json()[0]
        assert len(response.json()[0]) == 5

def test_valid_topic_and_length_no_available_links4():
    request_data = {
        "topic": "Python",
        "length": "medium",
        "user_id": "user1"
    }
    user_links = ["link1", "link2", "link3"]
    youtube_links = ["link1", "link2", "link3", "link4", "link5", "link6"]
    youtube_titles = ["title1", "title2", "title3", "title4", "title5","title6"]

    new_links = ["link7", "link8", "link9", "link10", "link11"]
    new_youtube_titles = ["title7", "title8", "title9", "title10", "title11"]
    with patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_by_topic_and_length",
               return_value=(youtube_links,youtube_titles)), \
            patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_user_by_topic_and_length",
                  return_value=user_links), \
            patch("server.utils.youtube.YouTubeService.connect_to_youtube_api", return_value=True), \
            patch("server.utils.youtube.YouTubeService.fetch_youtube_links", return_value=(new_links,new_youtube_titles)):
        response = client.post("/youtube/", json=request_data)
        assert response.status_code == 200
        new_links_set = set(new_links)
        count = sum(1 for link in response.json()[0] if link in new_links_set)
        assert len(response.json()[0]) == 5
        assert count >= 2


def test_invalid_youtube_connect():
    request_data = {
        "topic": "Python",
        "length": "medium",
        "user_id": "user1"
    }

    with patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_by_topic_and_length", return_value=([],[])), \
            patch("model.YouTube_DB.YouTubeMongoService.find_youtube_links_user_by_topic_and_length",
                  return_value=[]), \
            patch("server.utils.youtube.YouTubeService.connect_to_youtube_api", return_value=None):
        response = client.post("/youtube/", json=request_data)
        assert response.status_code == 500
        assert response.json() == {"detail": "Failed to connect to YouTube API"}
