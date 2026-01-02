from datetime import datetime
from typing import List, Optional

from beanie import Document as BeanieDocument, PydanticObjectId


class Document(BeanieDocument):
    name: str
    description: str
    file: str
    version: int
    project: List[PydanticObjectId]


class Comment(BeanieDocument):
    text: str
    description: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    author: List[PydanticObjectId]
    project: List[PydanticObjectId] = []
    task: List[PydanticObjectId] = []

