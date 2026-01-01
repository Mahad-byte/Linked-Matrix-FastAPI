from datetime import datetime
from typing import Optional
from typing import List

from beanie import Document, PydanticObjectId
from pydantic import BaseModel, Field
from bson import ObjectId

from utils.enums import Role


class User(Document):
    email: str
    password: str
    created_at: datetime
    profile: Optional[PydanticObjectId] = None
    project: List[PydanticObjectId] = Field(default_factory=list)


class Profile(Document):
    picture: Optional[str]
    role: Role
    user_id: PydanticObjectId


class Token(Document):
    access_token: str
    token_type: str
    user_id: str
