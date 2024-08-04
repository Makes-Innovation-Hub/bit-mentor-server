from fastapi import HTTPException, APIRouter
from googleapiclient.errors import HttpError
from server.utils.youtube import connect_to_youtube_api, fetch_youtube_links

router = APIRouter()


@router.get("/")
def get_youtube_links(topic: str, video_length: str):
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