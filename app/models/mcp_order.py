from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class Context(BaseModel):
    location: Optional[str] = Field(None, description="Ubicación física o lógica del usuario/dispositivo")
    time: Optional[str] = Field(None, description="Fecha y hora de la orden (ISO 8601)")
    area: Optional[str] = Field(None, description="Área de la casa o ambiente (ej: King's Bedroom, Living, Studio)")
    extra: Optional[Dict[str, Any]] = Field(None, description="Propiedades adicionales contextuales")

class MCPOrder(BaseModel):
    user: str = Field(..., description="Identificador del usuario que envía la orden")
    intent: str = Field(..., description="Acción a ejecutar sobre la entidad (ej: turn_on, play_media, etc.)")
    target: str = Field(..., description="Entidad objetivo de la acción (formato: domain.entity_id)")
    context: Optional[Context] = Field(None, description="Información contextual relevante para la orden")
    version: Optional[str] = Field(None, description="Versión del schema MCPOrder")

    class Config:
        schema_extra = {
            "example": {
                "user": "lucas",
                "intent": "turn_off",
                "target": "light.king_s_bedroom",
                "context": {
                    "area": "King's Bedroom",
                    "location": "home",
                    "time": "2025-07-22T21:45:00"
                },
                "version": "1.0.0"
            }
        }
