from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from core.database import get_jobs_collection
from utils.mongo import validate_object_id

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.delete(
    "/{job_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar oferta laboral"
)
def delete_job(
    job_id: str,
    collection: Collection = Depends(get_jobs_collection)
):
    """
    Eliminar permanentemente una oferta laboral de la colección ofertas por su _id en MongoDB.
    """
    if collection is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error de conexión con la base de datos"
        )

    obj_id = validate_object_id(job_id)

    try:
        result = collection.delete_one({"_id": obj_id})
    except PyMongoError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al eliminar la oferta laboral"
        )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Oferta laboral con ID '{job_id}' no encontrada"
        )

    return {
        "message": "Oferta laboral eliminada correctamente"
    }
