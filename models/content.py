from datetime import datetime
from typing import List

from beanie import Document, PydanticObjectId

from models.users import User


class Document(Document):
    name: str
    description: str
    file: str
    version: int
    project: List[PydanticObjectId]


class Comment(Document):
    text: str
    description: str
    created_at: datetime
    author: List[User]
    project: List[PydanticObjectId]
    task: List[PydanticObjectId]

