"""
FastAPI MCP Server - main entrypoint

Este archivo inicializa la aplicación FastAPI y monta los endpoints principales.

Uso:
    uvicorn app.main:app --reload

Documentación interactiva:
    http://localhost:8000/docs
    http://localhost:8000/redoc
"""

from fastapi import FastAPI
from app.api import endpoints

app = FastAPI(title="MCP Server", description="Prototype MCP server for LLM + Home Assistant integration.")

# Montar los endpoints principales
endpoints.include_routes(app)

# Ejemplo de ejecución:
# uvicorn app.main:app --reload
