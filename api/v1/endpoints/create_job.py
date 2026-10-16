from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobCreate, JobResponse
from utils.mongo import serialize_mongo_doc

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "",
    response_model=JobResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar oferta laboral"
)
def create_job(
    job_in: JobCreate,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Registrar una nueva oferta laboral en la colección ofertas de MongoDB.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    job_data = job_in.model_dump()
    job_data["postulantes"] = []

    try:
        result = collection.insert_one(job_data)
        job_data["_id"] = result.inserted_id
        return serialize_mongo_doc(job_data)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar la oferta laboral"
        )
