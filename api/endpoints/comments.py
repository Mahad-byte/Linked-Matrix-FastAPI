from fastapi import APIRouter, status
from beanie import PydanticObjectId
from datetime import datetime

from utils.helpers import create_notification
from models.content import Comment
from schemas.schema import ResponseSchema, CommentSchema
from schemas.update_schema import CommentUpdateSchema

router = APIRouter()


@router.post("/comments", status_code=status.HTTP_201_CREATED)
async def create_comment(payload: CommentSchema):
    created_at = payload.created_at or datetime.utcnow()
    comment = Comment(
        text=payload.text,
        description=payload.description,
        created_at=created_at,
        author=payload.author,
        project=payload.project,
        task=payload.task,
    )
    await comment.insert()
    await create_notification(
        user=str(payload.author),
        text="Task {task.title} created",      
    )
    return ResponseSchema(message="Success")


@router.get("/comments", status_code=status.HTTP_200_OK)
async def get_all_comments():
    return await Comment.find_all().to_list()


@router.get("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def get_specific_comment(comment_id: PydanticObjectId):
    return await Comment.get(comment_id)


@router.put("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def update_comment(comment_id: PydanticObjectId, payload: CommentUpdateSchema):
    comment = await Comment.get(comment_id)
    update_data = payload.dict(exclude_unset=True)

    await comment.set(update_data)
    return comment


@router.delete("/comments/{comment_id}", status_code=status.HTTP_200_OK)
async def delete_comment(comment_id: PydanticObjectId):
    comment = await Comment.get(comment_id)
    await comment.delete()
    return ResponseSchema(message="Success")
