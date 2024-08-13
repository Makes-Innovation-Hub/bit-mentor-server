from typing import List

from fastapi import HTTPException, APIRouter, Depends
from googleapiclient.errors import HttpError

from data_types.youtube_models import MarkLinkAsWatchedRequest, YouTubeLinkRequest
from model.YouTube_DB import YouTubeMongoService, get_db
from server.utils.logger import app_logger
from server.utils.youtube import YouTubeService, find_available_links
from constants import CATEGORIES

router = APIRouter()


@router.post("/")
def get_youtube_links(request: YouTubeLinkRequest, db: YouTubeMongoService = Depends(get_db)):
    app_logger.info(
        f"Received request to insert YouTube link: topic='{request.topic}', length='{request.length}', user_id='{request.user_id}'")

    # Validate length
    if request.length not in ["short", "medium", "long"]:
        app_logger.error(f"Invalid length: {request.length}")
        raise HTTPException(status_code=400, detail="Video length must be one of 'short', 'medium', or 'long'")

    # Validate topic
    if request.topic not in CATEGORIES:
        app_logger.error(f"Invalid topic: {request.topic}")
        raise HTTPException(status_code=400, detail="Invalid topic: topic should be in categories")

    # Retrieve existing links
    youtube_links = db.find_youtube_links_by_topic_and_length(request.topic, request.length) or []
    user_links = db.find_youtube_links_user_by_topic_and_length(request.topic, request.length, request.user_id) or []

    # Find available links
    available_links = find_available_links(youtube_links, user_links)

    if len(available_links) >= 5:
        available_links = available_links[:5]
        app_logger.info(f"Returning {len(available_links)} available links to the user.")
        return available_links
    else:
        youtube_service=YouTubeService()
        youtube = youtube_service.connect_to_youtube_api()
        if not youtube:
            raise HTTPException(status_code=500, detail="Failed to connect to YouTube API")

        try:
            video_links = youtube_service.fetch_youtube_links(youtube, request.topic, request.length)
            for link in video_links:
                db.add_youtube_link(request.topic, request.length, link)
                app_logger.info(f"Link {link} is added to youtube_links_collection.")

            # Update youtube_links with newly fetched links
            youtube_links.extend(video_links)

            available_links = find_available_links(youtube_links, user_links)
            if len(available_links) >= 5:
                available_links = available_links[:5]
                app_logger.info(f"Returning {len(available_links)} available links to the user.")
                return available_links
            else:
                app_logger.warning("Not enough videos found after fetching new links.")
                return []
        except Exception as e:
            app_logger.error(f"Error occurred while fetching video links: {str(e)}")
            raise HTTPException(status_code=500, detail="Error occurred while fetching video links")


@router.post("/mark_link_watched")
def mark_link_as_watched(request: MarkLinkAsWatchedRequest, db: YouTubeMongoService = Depends(get_db)) -> dict:
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
    print("links", youtube_links)
    # Validate video url
    if request.video_url not in youtube_links:
        app_logger.error(f"Invalid video URL: {request.video_url} URL does not exist in YouTube links")
        raise HTTPException(status_code=400, detail="Invalid video URL: URL does not exist in YouTube links")

    is_link_watched = db.link_exists_in_user_watched(request.user_id, request.topic, request.length, request.video_url)
    if is_link_watched:
        app_logger.error(f"Link already watched by user: {request.video_url}")
        raise HTTPException(status_code=400, detail="This link has already been watched by the user.")

    # Update the user's watched links list.
    db.update_user_stats(user_id=request.user_id, topic=request.topic, length=request.length,
                         video_url=request.video_url)
    app_logger.info(f"User stats updated successfully for user: {request.user_id}, video: {request.video_url}")
    return {"message": "User stats updated successfully"}
