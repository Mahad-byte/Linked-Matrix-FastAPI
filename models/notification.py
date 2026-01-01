from datetime import datetime
from typing import List

from pydantic import BaseModel
from beanie import Document

from models.users import User


class Notification(Document):
    text: str
    user: List[User]
    created_at: datetime
    mark_read: bool