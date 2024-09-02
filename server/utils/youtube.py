import random
from typing import List

from fastapi import HTTPException
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from server.utils.logger import app_logger
from setting.config import config


class YouTubeService:

    def connect_to_youtube_api(self) -> Resource:
        try:
            youtube = build('youtube', 'v3', developerKey=config.YOUTUBE_API)
            youtube.channels().list(part='id', forUsername='GoogleDevelopers').execute()
            return youtube
        except HttpError as e:
            return None
        except Exception as e:
            return None

    def fetch_youtube_links(self, youtube: Resource, topic: str, video_length: str):
        if not topic:
            raise HTTPException(status_code=400, detail="Topic cannot be an empty string")

        if video_length not in ["short", "medium", "long"]:
            raise HTTPException(status_code=400, detail="Video length must be one of 'short', 'medium', or 'long'")

        try:
            # Randomly select a variation to modify the topic,order_options
            variations = [' ', 'tutorial', 'guide', 'tips']
            topic_variation = topic + random.choice(variations)
            order_options = ['relevance', 'date', 'viewCount', 'rating']
            order_choice = random.choice(order_options)

            # Create and execute the request
            request = youtube.search().list(
                part='snippet',
                q=topic_variation,
                type='video',
                videoDuration=video_length,
                maxResults=5,
                order=order_choice
            )
            response = request.execute()

            # Extract video links and titles
            video_links = [
                f"https://www.youtube.com/watch?v={item['id']['videoId']}"
                for item in response['items']
            ]
            video_titles = [
                item['snippet']['title']
                for item in response['items']
            ]
            return video_links, video_titles

        except HttpError as e:
            raise HTTPException(status_code=400, detail=f"An HTTP error occurred while fetching YouTube links: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"An error occurred while fetching YouTube links: {e}")


def find_available_links(youtube_links, user_links):
    """
    Finds available YouTube links that have not been watched by the user.
    Returns a list of available links.
    """
    # Convert lists to sets
    youtube_links_set = set(youtube_links or [])
    user_links_set = set(user_links or [])

    # Find the difference
    available_links_set = list(youtube_links_set - user_links_set)

    app_logger.info(f"Found {len(available_links_set)} available links not watched by user.")
    return available_links_set
