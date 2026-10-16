import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse
from utils.mongo import serialize_mongo_docs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/filter/location",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar ofertas laborales por ubicación"
)
def filter_jobs_by_location(
    location: str = Query(..., description="Ubicación o ciudad a filtrar (coincidencia parcial)"),
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Filtrar ofertas laborales por coincidencias parciales (case-insensitive) en el campo ubicacion.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    cleaned_location = location.strip()
    if not cleaned_location:
        raise HTTPException(
            status_code=422,
            detail="El parámetro 'location' no puede estar vacío ni contener solo espacios"
        )

    escaped_location = re.escape(cleaned_location)

    try:
        cursor = collection.find({
            "ubicacion": {"$regex": escaped_location, "$options": "i"}
        })
        matching_jobs = list(cursor)
        return serialize_mongo_docs(matching_jobs)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al filtrar las ofertas laborales por ubicación"
        )
