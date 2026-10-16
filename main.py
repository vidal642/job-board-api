from fastapi import FastAPI
from core.database import check_database_connection
from api.v1.router import api_router

app = FastAPI(
    title="Job Board API",
    description="API REST para bolsa de trabajo utilizando FastAPI y MongoDB.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(api_router, prefix="/api/v1")


@app.get("/", tags=["General"])
def root():
    return {
        "message": "Bienvenido a la API de Bolsa de Trabajo",
        "status": "online"
    }


@app.get("/health", tags=["General"])
def health():
    is_db_connected = check_database_connection()
    return {
        "status": "ok",
        "database": "connected" if is_db_connected else "disconnected"
    }
