from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

from models.project import Project
from utils.enums import Role, Status


class RegisterSchema(BaseModel):
    email: str
    password: str
    confirm_password: str
    role: Role
    picture: Optional[str] = None 


class ProfileSchema(BaseModel):
    role: Role
    user_id: PydanticObjectId



class LoginSchema(BaseModel):
    email: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    token_type: str
    

class ResponseSchema(BaseModel):
    message: str


class ProjectSchema(BaseModel):
    title: str
    start_date: datetime
    end_date: datetime


class TaskSchema(BaseModel):
    title: str
    description: str
    status: Status
    project: List[PydanticObjectId] # One - Many
    asignee: List[PydanticObjectId]


class DocumentSchema(BaseModel):
    name: str
    description: Optional[str] = None
    file: Optional[str] = None
    version: int
    project: List[PydanticObjectId] = []


class CommentSchema(BaseModel):
    text: str
    description: Optional[str] = None
    created_at: datetime = datetime.utcnow()
    author: List[PydanticObjectId]
    project: List[PydanticObjectId] = []
    task: List[PydanticObjectId] = []


class NotificationCreateSchema(BaseModel):
    text: str
    user: List[PydanticObjectId]
    mark_read: bool
