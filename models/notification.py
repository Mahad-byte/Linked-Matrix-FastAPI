from datetime import datetime
from typing import List

from pydantic import BaseModel
from beanie import Document, PydanticObjectId

from models.users import User


class Notification(Document):
    text: str
    user: PydanticObjectId
    created_at: datetime
    mark_read: bool