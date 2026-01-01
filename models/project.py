from datetime import datetime
from typing import List

from beanie import Document, PydanticObjectId

from utils.enums import Status
from utils.enums import EventType


class Project(Document):
    title: str
    start_date: datetime
    end_date: datetime
    created_by: PydanticObjectId
    team_members: List[PydanticObjectId] = [] # Many - Many


class Tasks(Document):
    title: str
    description: str
    status: Status
    project: List[PydanticObjectId] # One - Many
    asignee: List[PydanticObjectId]


class Timeline(Document):
    event_type: EventType
    time: datetime
    project: List[PydanticObjectId] = []
