from fastapi import APIRouter, status
from beanie import PydanticObjectId

from models.project import Tasks
from schemas.schema import ResponseSchema, TaskSchema
from schemas.update_schema import TaskUpdateSchema
from utils.helpers import create_notification


router = APIRouter()


@router.post("/tasks", status_code=status.HTTP_201_CREATED)
async def create_task(payload: TaskSchema):
    
    task = Tasks(title=payload.title, description=payload.description, 
                      status=payload.status, project=payload.project, asignee=payload.asignee)
    await task.insert()
    await create_notification(
        user=str(payload.asignee),
        text="Task {task.title} created",      
    )
    return ResponseSchema(message="Success")


@router.get("/tasks", status_code=status.HTTP_200_OK)
async def get_all_tasks():
    return await Tasks.find_all().to_list()


@router.get("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_specific_tasks(task_id: PydanticObjectId):
    return await Tasks.get(task_id)


@router.put("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def get_task_with_id(task_id: PydanticObjectId, payload: TaskUpdateSchema):
    print(task_id)
    task = await Tasks.get(task_id)
    update_data = payload.dict(exclude_unset=True)

    await task.set(update_data)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_200_OK)
async def delete_task_with_id(task_id: PydanticObjectId):
        task = await Tasks.get(task_id)
        await task.delete()
        return ResponseSchema(message="Success")
