import math
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse
from utils.mongo import serialize_mongo_docs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "/filter/salary",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Filtrar ofertas laborales por rango salarial"
)
def filter_jobs_by_salary(
    min_salary: Optional[float] = Query(None, description="Salario mínimo (inclusivo)"),
    max_salary: Optional[float] = Query(None, description="Salario máximo (inclusivo)"),
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Filtrar ofertas laborales según un rango salarial (operadores $gte y $lte).
    Se requiere al menos uno de los parámetros: min_salary o max_salary.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    if min_salary is None and max_salary is None:
        raise HTTPException(
            status_code=422,
            detail="Debe proporcionar al menos uno de los parámetros: 'min_salary' o 'max_salary'"
        )

    if min_salary is not None:
        if math.isnan(min_salary) or math.isinf(min_salary):
            raise HTTPException(
                status_code=422,
                detail="El parámetro 'min_salary' debe ser un número finito válido"
            )
        if min_salary < 0:
            raise HTTPException(
                status_code=422,
                detail="El parámetro 'min_salary' no puede ser negativo"
            )

    if max_salary is not None:
        if math.isnan(max_salary) or math.isinf(max_salary):
            raise HTTPException(
                status_code=422,
                detail="El parámetro 'max_salary' debe ser un número finito válido"
            )
        if max_salary < 0:
            raise HTTPException(
                status_code=422,
                detail="El parámetro 'max_salary' no puede ser negativo"
            )

    if min_salary is not None and max_salary is not None:
        if min_salary > max_salary:
            raise HTTPException(
                status_code=422,
                detail="El salario mínimo no puede ser mayor que el salario máximo"
            )

    salary_filter = {}
    if min_salary is not None:
        salary_filter["$gte"] = min_salary
    if max_salary is not None:
        salary_filter["$lte"] = max_salary

    query = {"salario": salary_filter}

    try:
        cursor = collection.find(query)
        matching_jobs = list(cursor)
        return serialize_mongo_docs(matching_jobs)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al filtrar las ofertas laborales por rango salarial"
        )
