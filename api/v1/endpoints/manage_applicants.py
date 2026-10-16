from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import ApplicantCreate, ApplicantResponse
from utils.mongo import validate_object_id

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post(
    "/{job_id}/applicants",
    response_model=ApplicantResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar postulante en una oferta laboral"
)
def apply_to_job(
    job_id: str,
    applicant_in: ApplicantCreate,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Registrar un postulante dentro del arreglo 'postulantes' de la oferta laboral especificada.
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
            detail=f"No se encontró la oferta laboral con ID '{job_id}'"
        )

    applicant_data = applicant_in.model_dump()

    try:
        collection.update_one(
            {"_id": obj_id},
            {"$push": {"postulantes": applicant_data}}
        )
        return applicant_data
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al registrar el postulante en la oferta laboral"
        )


@router.get(
    "/{job_id}/applicants",
    response_model=List[ApplicantResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar postulantes de una oferta laboral"
)
def list_job_applicants(
    job_id: str,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Consultar los postulantes registrados en una oferta laboral específica.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    obj_id = validate_object_id(job_id)

    try:
        job = collection.find_one({"_id": obj_id}, {"postulantes": 1})
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar los postulantes de la oferta laboral"
        )

    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró la oferta laboral con ID '{job_id}'"
        )

    applicants = job.get("postulantes") or []
    return applicants
