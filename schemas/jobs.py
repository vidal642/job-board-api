import re
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.[a-zA-Z]{2,}$")


class EmpresaInfo(BaseModel):
    nombre: str = Field(..., min_length=2, max_length=100, description="Nombre de la empresa")
    contacto: str = Field(..., min_length=5, max_length=100, description="Correo o contacto de la empresa")


class ApplicantCreate(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre completo del postulante")
    email: str = Field(..., min_length=5, max_length=100, description="Correo electrónico del postulante")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "nombre": "Juan Pérez",
                "email": "juan.perez@example.com"
            }
        }
    )

    @field_validator("nombre")
    @classmethod
    def validate_nombre(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("El nombre no puede estar vacío ni contener solo espacios")
        return cleaned

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        cleaned = v.strip()
        if not cleaned:
            raise ValueError("El correo electrónico no puede estar vacío")
        if not EMAIL_REGEX.match(cleaned):
            raise ValueError("Formato de correo electrónico inválido")
        return cleaned


class ApplicantResponse(BaseModel):
    nombre: str = Field(..., description="Nombre completo del postulante")
    email: str = Field(..., description="Correo electrónico del postulante")

    model_config = ConfigDict(from_attributes=True, extra="forbid")


PostulanteResponse = ApplicantResponse


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


class JobUpdate(BaseModel):
    titulo: Optional[str] = Field(default=None, min_length=3, max_length=150, description="Título del puesto laboral")
    descripcion: Optional[str] = Field(default=None, min_length=10, max_length=5000, description="Descripción del puesto")
    empresa: Optional[str] = Field(default=None, min_length=2, max_length=100, description="Nombre de la empresa")
    ubicacion: Optional[str] = Field(default=None, min_length=2, max_length=100, description="Ubicación o ciudad")
    modalidad: Optional[str] = Field(default=None, min_length=3, max_length=50, description="Modalidad de trabajo")
    salario: Optional[float] = Field(default=None, ge=0, description="Salario ofrecido (no negativo)")
    tipo_contrato: Optional[str] = Field(default=None, min_length=3, max_length=50, description="Tipo de contrato")
    estado: Optional[str] = Field(default=None, description="Estado de la oferta")
    requisitos: Optional[List[str]] = Field(default=None, description="Lista de requisitos")
    empresa_info: Optional[EmpresaInfo] = Field(default=None, description="Información de contacto de la empresa")

    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={
            "example": {
                "salario": 5200.0,
                "modalidad": "Híbrido",
                "estado": "Cerrada"
            }
        }
    )

    @model_validator(mode="after")
    def validate_has_editable_fields(self):
        fields = [
            self.titulo, self.descripcion, self.empresa, self.ubicacion,
            self.modalidad, self.salario, self.tipo_contrato, self.estado,
            self.requisitos, self.empresa_info
        ]
        if not any(val is not None for val in fields):
            raise ValueError("Debe proporcionar al menos un campo editable para actualizar la oferta laboral.")
        return self


class JobResponse(JobBase):
    id: str = Field(..., alias="_id", description="Identificador único de la oferta")
    postulantes: List[PostulanteResponse] = Field(
        default_factory=list,
        description="Lista de postulantes registrados"
    )

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)
