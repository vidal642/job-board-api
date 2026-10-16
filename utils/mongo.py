from typing import Any, Dict, List
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status


def validate_object_id(id_str: str) -> ObjectId:
    """Validate and convert string to MongoDB ObjectId."""
    try:
        return ObjectId(id_str)
    except (InvalidId, TypeError, ValueError):
        raise HTTPException(
            status_code=422,
            detail=f"Formato de identificador inválido: '{id_str}'"
        )


def serialize_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """Convert MongoDB document _id to string for JSON serialization."""
    if not doc:
        return doc
    doc_copy = dict(doc)
    if "_id" in doc_copy:
        doc_copy["_id"] = str(doc_copy["_id"])
        doc_copy["id"] = str(doc_copy["_id"])
    return doc_copy


def serialize_mongo_docs(docs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Convert a list of MongoDB documents."""
    return [serialize_mongo_doc(doc) for doc in docs]
