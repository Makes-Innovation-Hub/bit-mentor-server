from typing import List

from fastapi import HTTPException
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from setting.config import config


def connect_to_youtube_api() -> Resource:
    try:
        youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API)
        youtube.channels().list(part='id', forUsername='GoogleDevelopers').execute()
        return youtube
    except HttpError as e:
        return None
    except Exception as e:
        return None


def fetch_youtube_links(youtube: Resource, topic: str, video_length: str) -> List[str]:
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be an empty string")

        # Validate video_length
    if video_length not in ["short", "medium", "long"]:
        raise HTTPException(status_code=400, detail="Video length must be one of 'short', 'medium', or 'long'")
    try:
        request = youtube.search().list(
            part='snippet',
            q=topic,
            type='video',
            videoDuration=video_length,
            maxResults=5
        )
        response = request.execute()
        video_links = [
            f"https://www.youtube.com/watch?v={item['id']['videoId']}"
            for item in response['items']
        ]
        return video_links
    except HttpError as e:
        raise HTTPException(status_code=400, detail=f"An HTTP error occurred while fetching YouTube links: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred while fetching YouTube links: {e}")
