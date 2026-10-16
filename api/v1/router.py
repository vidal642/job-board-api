from fastapi import APIRouter
from api.v1.endpoints import create_job

api_router = APIRouter()
api_router.include_router(create_job.router)
