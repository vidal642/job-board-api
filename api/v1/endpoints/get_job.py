from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse
from utils.mongo import serialize_mongo_doc, validate_object_id

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Consultar oferta laboral por ID"
)
def get_job(
    job_id: str,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Consultar una oferta laboral específica por su identificador _id en MongoDB.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    obj_id = validate_object_id(job_id)

    try:
        job = collection.find_one({"_id": obj_id})
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar la oferta laboral"
        )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID '{job_id}' no encontrada"
        )

    return serialize_mongo_doc(job)
