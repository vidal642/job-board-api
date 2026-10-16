from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from schemas.jobs import JobResponse
from utils.mongo import serialize_mongo_docs

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.get(
    "",
    response_model=List[JobResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar ofertas laborales"
)
def list_jobs(
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Consultar todas las ofertas laborales registradas en la colección ofertas de MongoDB.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    try:
        jobs_cursor = collection.find()
        jobs_list = list(jobs_cursor)
        return serialize_mongo_docs(jobs_list)
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al consultar las ofertas laborales"
        )
