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
    "/search",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Buscar ofertas laborales por título"
)
def search_jobs(
    title: str = Query(..., description="Texto o palabra clave a buscar en el título de la oferta"),
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Buscar ofertas laborales por coincidencias parciales (case-insensitive) en el título.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    cleaned_title = title.strip()
    if not cleaned_title:
        raise HTTPException(
            status_code=422,
            detail="El parámetro de búsqueda 'title' no puede estar vacío ni contener solo espacios"
        )

    escaped_title = re.escape(cleaned_title)

    try:
        cursor = collection.find({
            "titulo": {"$regex": escaped_title, "$options": "i"}
        })
        matching_jobs = list(cursor)
        return serialize_mongo_docs(matching_jobs)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al buscar las ofertas laborales"
        )
