from fastapi import APIRouter
from api.v1.endpoints import create_job, list_jobs

api_router = APIRouter()
api_router.include_router(create_job.router)
api_router.include_router(list_jobs.router)
