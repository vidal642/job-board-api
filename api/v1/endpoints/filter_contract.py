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
    "/filter/contract",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar ofertas laborales por tipo de contrato"
)
def filter_jobs_by_contract(
    contract_type: str = Query(..., description="Tipo de contrato a filtrar (coincidencia exacta, case-insensitive)"),
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Filtrar ofertas laborales por coincidencia exacta (case-insensitive) en el campo tipo_contrato.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    cleaned_contract = contract_type.strip()
    if not cleaned_contract:
        raise HTTPException(
            status_code=422,
            detail="El parámetro 'contract_type' no puede estar vacío ni contener solo espacios"
        )

    escaped_contract = re.escape(cleaned_contract)
    regex_pattern = f"^{escaped_contract}$"

    try:
        cursor = collection.find({
            "tipo_contrato": {"$regex": regex_pattern, "$options": "i"}
        })
        matching_jobs = list(cursor)
        return serialize_mongo_docs(matching_jobs)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al filtrar las ofertas laborales por tipo de contrato"
        )
