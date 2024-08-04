import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
from fastapi import HTTPException
from googleapiclient.errors import HttpError

from server.server import app
from server.utils.youtube import connect_to_youtube_api, fetch_youtube_links
from setting.config import config

client = TestClient(app)


# MISSING INPUT
# missing topic input
def test_get_youtube_links_missing_topic():
    response = client.get("youtube/?video_length=medium")
    assert response.status_code == 400
    assert response.json() == {"detail": "Topic cannot be an empty string"}


# missing video length input
def test_get_youtube_links_missing_video_length():
    response = client.get("youtube/?topic=Python")
    assert response.status_code == 400
    assert response.json() == {"detail": "Video length must be one of 'short', 'medium', or 'long'"}


# missing topic and video length inputs
def test_get_youtube_links_missing_both():
    response = client.get("youtube/")
    assert response.status_code == 400  # Unprocessable Entity
    assert "detail" in response.json()


def test_fetch_youtube_links_missing_topic():
    mock_youtube = Mock()

    with pytest.raises(HTTPException) as e:
        fetch_youtube_links(mock_youtube, '', 'medium')

    assert e.value.status_code == 400
    assert e.value.detail == "Topic cannot be an empty string"


def test_fetch_youtube_links_missing_vedio_length():
    mock_youtube = Mock()

    with pytest.raises(HTTPException) as e:
        fetch_youtube_links(mock_youtube, 'python', '')

    assert e.value.status_code == 400
    assert e.value.detail == "Video length must be one of 'short', 'medium', or 'long'"


########################################################################################################################
# WRONG INPUT
# invalid video length input
def test_get_youtube_links_invalid_video_length():
    response = client.get("/youtube/?topic=Python&video_length=111111111")
    assert response.status_code == 400
    assert response.json() == {"detail": "Video length must be one of 'short', 'medium', or 'long'"}


def test_get_youtube_links_invalid2_video_length():
    response = client.get("/youtube/?topic=Python&video_length=""")
    assert response.status_code == 400
    assert response.json() == {"detail": "Video length must be one of 'short', 'medium', or 'long'"}


# invalid topic input
def test_get_youtube_links_invalid_topic():
    response = client.get("/youtube/?topic=""&video_length=medium")
    assert response.status_code == 400
    assert response.json() == {"detail": "Topic cannot be an empty string"}


def test_fetch_youtube_links_invalid_vedio_length():
    mock_youtube = Mock()

    with pytest.raises(HTTPException) as e:
        fetch_youtube_links(mock_youtube, 'python', 'sdf')

    assert e.value.status_code == 400
    assert e.value.detail == "Video length must be one of 'short', 'medium', or 'long'"


########################################################################################################################


def test_get_youtube_links_success():
    response = client.get("youtube/?topic=Python&video_length=medium")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_get_youtube_links_success2():
    response = client.get("youtube/?video_length=medium&topic=Python")
    assert response.status_code == 200
    assert len(response.json()) == 5

########################################################################################################################


def test_fetch_youtube_links_youtube_none():
    with pytest.raises(HTTPException) as e:
        fetch_youtube_links(None, 'Python', 'medium')

    assert e.value.status_code == 500
    assert "An error occurred while fetching YouTube links:" in e.value.detail


def test_fetch_youtube_links_success():
    mock_youtube = Mock()
    mock_search = Mock()
    mock_list = Mock()

    # Set up the method chain
    mock_youtube.search.return_value = mock_search
    mock_search.list.return_value = mock_list
    mock_list.execute.return_value = {
        'items': [
            {'id': {'videoId': 'link1'}},
            {'id': {'videoId': 'link2'}},
            {'id': {'videoId': 'link3'}},
            {'id': {'videoId': 'link4'}},
            {'id': {'videoId': 'link5'}}
        ]
    }

    video_links = fetch_youtube_links(mock_youtube, 'Python', 'medium')

    assert len(video_links) == 5
    assert video_links == [
        "https://www.youtube.com/watch?v=link1",
        "https://www.youtube.com/watch?v=link2",
        "https://www.youtube.com/watch?v=link3",
        "https://www.youtube.com/watch?v=link4",
        "https://www.youtube.com/watch?v=link5"
    ]
