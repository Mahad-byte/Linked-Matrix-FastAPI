from fastapi import APIRouter, status, HTTPException
from beanie import PydanticObjectId
from datetime import datetime

from models.notification import Notification
from schemas.schema import ResponseSchema, NotificationCreateSchema

router = APIRouter()


@router.post("/notifications", status_code=status.HTTP_201_CREATED)
async def create_notification(payload: NotificationCreateSchema):
    notification = Notification(
        text=payload.text,
        user=payload.user,
        created_at=datetime.utcnow(),
        mark_read=False,
    )
    await notification.insert()
    return ResponseSchema(message="Success")


@router.get("/notifications", status_code=status.HTTP_200_OK)
async def get_all_notifications():
    return await Notification.find_all().to_list()


@router.put("/notifications/{notification_id}/mark_read", status_code=status.HTTP_200_OK)
async def mark_notification_read(notification_id: PydanticObjectId):
    notification = await Notification.get(notification_id)
    await notification.set({"mark_read": True})
    return notification
