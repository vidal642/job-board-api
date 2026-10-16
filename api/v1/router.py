from fastapi import APIRouter
from api.v1.endpoints import (
    create_job,
    list_jobs,
    search_jobs,
    filter_modality,
    get_job,
    update_job,
    delete_job,
)

api_router = APIRouter()
api_router.include_router(create_job.router)
api_router.include_router(list_jobs.router)
api_router.include_router(search_jobs.router)
api_router.include_router(filter_modality.router)
api_router.include_router(get_job.router)
api_router.include_router(update_job.router)
api_router.include_router(delete_job.router)
