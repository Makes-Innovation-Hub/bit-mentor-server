from pydantic import BaseModel


class MarkLinkAsWatchedRequest(BaseModel):
    user_id: str
    topic: str
    length: str
    video_url: str

class YouTubeLinkRequest(BaseModel):
    topic: str
    length: str
    user_id: str