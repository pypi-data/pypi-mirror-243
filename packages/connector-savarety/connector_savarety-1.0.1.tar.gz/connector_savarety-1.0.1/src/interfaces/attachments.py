from typing import Optional

from pydantic import BaseModel

from src.interfaces.photo import Photo
from src.interfaces.video import Video


class Attachment(BaseModel):
    type: str
    photo: Optional[Photo] = None
    video: Optional[Video] = None
    text: Optional[str] = None
    user_id: Optional[int] = None
    owner_id: Optional[int] = None
    web_view_token: Optional[str] = None
    description: Optional[str] = None
    duration: Optional[int] = None


class RequestAttachments(BaseModel):
    data: list[Attachment]
