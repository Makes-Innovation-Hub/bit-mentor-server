from typing import List

from fastapi import HTTPException, APIRouter, Depends
from googleapiclient.errors import HttpError

from data_types.youtube_models import MarkLinkAsWatchedRequest
from model.YouTube_DB import YouTubeService, get_db
from server.utils.logger import app_logger
from server.utils.youtube import connect_to_youtube_api, fetch_youtube_links
from constants import CATEGORIES

router = APIRouter()


@router.get("/", response_model=List[str])
def get_youtube_links(topic: str, video_length: str) -> List[str]:
    """
    Fetch YouTube video links based on a given topic and video length.

    Args:
        topic (str): The topic to fetch video links for. Must be a non-empty string.
        video_length (str): The length category of the videos to fetch. Must be one of 'short', 'medium', or 'long'.

    Returns:
        List[str]: A list of URLs as strings.
    """

    # Validate topic
    if not topic:
        raise HTTPException(status_code=400, detail="Topic cannot be an empty string")

    # Validate video_length
    if video_length not in ["short", "medium", "long"]:
        raise HTTPException(status_code=400, detail="Video length must be one of 'short', 'medium', or 'long'")

    # Connect to the YouTube API
    youtube = connect_to_youtube_api()
    if not youtube:
        raise HTTPException(status_code=500, detail="Failed to connect to YouTube API")

    try:
        video_links = fetch_youtube_links(youtube, topic, video_length)
        # returning a list of URLs as strings
        return video_links
    except HttpError as e:
        raise HTTPException(status_code=400, detail=f"An HTTP error occurred while fetching YouTube links: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"An error occurred while fetching YouTube links: {str(e)}")


@router.post("/mark_link_watched")
def mark_link_as_watched(request: MarkLinkAsWatchedRequest, db: YouTubeService = Depends(get_db)) -> dict:
    """
    Mark a YouTube link as watched for a specific user.

    :param request: The request body containing the user ID, topic, length, and video URL.
    :param db: The YouTubeService instance used to interact with MongoDB
    :return: dict: A success message indicating that the user's stats were updated successfully.
    """
    app_logger.info(f"Received request to mark link as watched: {request.dict()}")

    # Validate inputs
    if request.length not in ["short", "medium", "long"]:
        app_logger.error(f"Invalid length: {request.length}")
        raise HTTPException(status_code=400, detail="Video length must be one of 'short', 'medium', or 'long'")
    if request.topic not in CATEGORIES:
        app_logger.error(f"Invalid topic: {request.topic}")
        raise HTTPException(status_code=400, detail="Invalid topic: topic should be in categories")

    #  initialize the user.
    db.initialize_user(request.user_id)
    app_logger.info(f"Initialized user: {request.user_id}")

    # check if url exist in youtube_links_collection
    youtube_links = db.find_youtube_links_by_topic_and_length(request.topic, request.length)

    # Validate video url
    if request.video_url not in youtube_links:
        app_logger.error(f"Invalid video URL: {request.video_url} URL does not exist in YouTube links")
        raise HTTPException(status_code=400, detail="Invalid video URL: URL does not exist in YouTube links")

    is_link_watched = db.link_exists_in_user_watched(request.user_id, request.topic, request.length, request.video_url)
    if is_link_watched:
        app_logger.error(f"Link already watched by user: {request.video_url}")
        raise HTTPException(status_code=400, detail="This link has already been watched by the user.")

    # Update the user's watched links list.
    db.update_user_stats(user_id=request.user_id,topic=request.topic,length=request.length,video_url=request.video_url)
    app_logger.info(f"User stats updated successfully for user: {request.user_id}, video: {request.video_url}")
    return {"message": "User stats updated successfully"}
