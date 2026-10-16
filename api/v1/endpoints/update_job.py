from fastapi import APIRouter, Depends, HTTPException, status
from pymongo import ReturnDocument
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse, JobUpdate
from utils.mongo import serialize_mongo_doc, validate_object_id

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.put(
    "/{job_id}",
    response_model=JobResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar oferta laboral"
)
def update_job(
    job_id: str,
    job_in: JobUpdate,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Actualizar los campos especificados de una oferta laboral existente en MongoDB.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    obj_id = validate_object_id(job_id)

    update_data = job_in.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=422,
            detail="Debe proporcionar al menos un campo editable para actualizar"
        )

    try:
        updated_job = collection.find_one_and_update(
            {"_id": obj_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER
        )
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al actualizar la oferta laboral"
        )

    if not updated_job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID '{job_id}' no encontrada"
        )

    return serialize_mongo_doc(updated_job)
