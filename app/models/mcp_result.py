from pydantic import BaseModel, Field
from typing import Optional

class MCPResult(BaseModel):
    status: str = Field(..., description="Resultado de la acción ejecutada (success o error)")
    action: str = Field(..., description="Acción ejecutada sobre la entidad (ej: turn_off)")
    target: str = Field(..., description="Entidad objetivo de la acción (formato: domain.entity_id)")
    message: Optional[str] = Field(None, description="Mensaje descriptivo para el usuario")
    error_code: Optional[str] = Field(None, description="Código de error devuelto por Home Assistant (si aplica)")
    version: Optional[str] = Field(None, description="Versión del schema MCPResult")
    request_id: Optional[str] = Field(None, description="Identificador único de la request para trazabilidad")
    timestamp: Optional[str] = Field(None, description="Fecha y hora de la respuesta (ISO 8601)")

    class Config:
        schema_extra = {
            "example": {
                "status": "success",
                "action": "turn_off",
                "target": "light.king_s_bedroom",
                "message": "The light in King's Bedroom has been turned off.",
                "version": "1.0.0",
                "request_id": "abc123",
                "timestamp": "2025-07-22T21:45:01"
            }
        }
