from fastapi import APIRouter

from api.endpoints import auth, project, task


api_router = APIRouter(prefix='/api')

api_router.include_router(auth.router)
api_router.include_router(project.router)
api_router.include_router(task.router)
