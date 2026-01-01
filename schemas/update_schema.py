from beanie import PydanticObjectId
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from typing import List

from utils.enums import Status


class ProjectUpdateSchema(BaseModel):
    title: Optional[str] = None
    end_date: Optional[datetime] = None
    team_members: Optional[List[PydanticObjectId]] = None


class TaskUpdateSchema(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[Status] = None
    project: Optional[List[PydanticObjectId]] = None # One - Many
    asignee: Optional[List[PydanticObjectId]] = None


class DocumentUpdateSchema(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    file: Optional[str] = None
    version: Optional[int] = None
    project: Optional[List[PydanticObjectId]] = None
