import re
from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse
from utils.mongo import serialize_mongo_docs

router = APIRouter(prefix="/jobs", tags=["Jobs"])

ALLOWED_MODALITIES = {"presencial", "remoto", "hibrido", "híbrido"}


@router.get(
    "/filter/modality",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar ofertas laborales por modalidad"
)
def filter_jobs_by_modality(
    modality: str = Query(..., description="Modalidad de trabajo a filtrar: Presencial, Remoto, Híbrido"),
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Filtrar ofertas laborales por coincidencia exacta (case-insensitive) en el campo modalidad.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    cleaned_modality = modality.strip()
    if not cleaned_modality:
        raise HTTPException(
            status_code=422,
            detail="El parámetro 'modality' no puede estar vacío ni contener solo espacios"
        )

    modality_lower = cleaned_modality.lower()
    if modality_lower not in ALLOWED_MODALITIES:
        raise HTTPException(
            status_code=422,
            detail=f"Modalidad no permitida: '{cleaned_modality}'. Valores permitidos: Presencial, Remoto, Híbrido"
        )

    # Construir regex exacto insensible a mayúsculas y tolerante a tilde en Híbrido/Hibrido
    if modality_lower in ("hibrido", "híbrido"):
        regex_pattern = r"^h[ií]brido$"
    else:
        regex_pattern = f"^{re.escape(modality_lower)}$"

    try:
        cursor = collection.find({
            "modalidad": {"$regex": regex_pattern, "$options": "i"}
        })
        matching_jobs = list(cursor)
        return serialize_mongo_docs(matching_jobs)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al filtrar las ofertas laborales"
        )
