from fastapi import APIRouter, status, Depends
from beanie import PydanticObjectId

from models.project import Project
from models.users import User
from schemas.schema import ResponseSchema, ProjectSchema
from schemas.update_schema import ProjectUpdateSchema
from utils.helpers import init_auth_helper, role
from utils.enums import Role

router = APIRouter()

auth_helper = init_auth_helper()


@router.post("/projects", status_code=status.HTTP_201_CREATED)
@role.required(Role.PM)
async def create_project(payload: ProjectSchema, current_user: User):
    project = Project(
        title=payload.title,
        start_date=payload.start_date,
        end_date=payload.end_date,
        created_by=current_user.id,
        team_members=[],
    )
    await project.insert()
    return ResponseSchema(message="Success")


@router.get("/projects", status_code=status.HTTP_200_OK)
async def get_all_projects():
    return await Project.find_all().to_list()


@router.get("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def get_specific_projects(project_id: PydanticObjectId):
    return await Project.get(project_id)


@router.put("/projects/{project_id}", status_code=status.HTTP_200_OK)
async def get_project_with_id(
    project_id: PydanticObjectId, payload: ProjectUpdateSchema
):
    print(project_id)
    project = await Project.get(project_id)
    update_data = payload.dict(exclude_unset=True)

    await project.set(update_data)
    return project


@router.delete("/projects/{project_id}", status_code=status.HTTP_200_OK)
@role.required(Role.PM)
async def delete_project_with_id(project_id: PydanticObjectId, current_user: User = None):
    project = await Project.get(project_id)
    await project.delete()
    return ResponseSchema(message="Success")
