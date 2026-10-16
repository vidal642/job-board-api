from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class EmpresaInfo(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la empresa")
    contacto: str = Field(..., min_length=5, max_length=100, description="Correo o contacto de la empresa")


class PostulanteResponse(BaseModel):
    id: Optional[str] = Field(default=None, description="Identificador único del postulante")
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre completo del postulante")
    correo: str = Field(..., min_length=5, max_length=100, description="Correo electrónico del postulante")
    fecha_postulacion: Optional[datetime] = Field(default=None, description="Fecha y hora de postulación")

    model_config = ConfigDict(from_attributes=True)


class JobBase(BaseModel):
    titulo: str = Field(..., min_length=3, max_length=150, description="Título del puesto laboral")
    descripcion: str = Field(..., min_length=10, max_length=5000, description="Descripción del puesto")
    empresa: str = Field(..., min_length=2, max_length=100, description="Nombre de la empresa")
    ubicacion: str = Field(..., min_length=2, max_length=100, description="Ubicación o ciudad")
    modalidad: str = Field(..., min_length=3, max_length=50, description="Modalidad de trabajo")
    salario: float = Field(..., ge=0, description="Salario ofrecido (no negativo)")
    tipo_contrato: str = Field(..., min_length=3, max_length=50, description="Tipo de contrato")
    estado: str = Field(default="Activa", description="Estado de la oferta")
    requisitos: List[str] = Field(default_factory=list, description="Lista de requisitos")
    empresa_info: EmpresaInfo = Field(..., description="Información de contacto de la empresa")


class JobCreate(JobBase):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "titulo": "Desarrollador Backend",
                "descripcion": "Desarrollo de aplicaciones y servicios web con FastAPI y MongoDB.",
                "empresa": "Tech Solutions",
                "ubicacion": "Cochabamba",
                "modalidad": "Remoto",
                "salario": 4500.0,
                "tipo_contrato": "Tiempo completo",
                "estado": "Activa",
                "requisitos": [
                    "Python",
                    "FastAPI",
                    "MongoDB"
                ],
                "empresa_info": {
                    "nombre": "Tech Solutions",
                    "contacto": "contacto@techsolutions.com"
                }
            }
        }
    )


class JobResponse(JobBase):
    id: str = Field(..., alias="_id", description="Identificador único de la oferta")
    postulantes: List[PostulanteResponse] = Field(
        default_factory=list,
        description="Lista de postulantes registrados"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
