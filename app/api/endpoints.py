"""
Endpoints principales del MCP Server

- POST /mcp/order: Recibe y valida una orden MCP
- GET /health: Healthcheck básico
"""
from fastapi import APIRouter, Request, Response, status, FastAPI, Body
from fastapi.responses import JSONResponse
from app.models.mcp_order import MCPOrder
from app.models.mcp_result import MCPResult
from app.core.validation import validate_mcp_order_jsonschema
from jsonschema import ValidationError as JSONSchemaValidationError
from pydantic import ValidationError as PydanticValidationError
import datetime
import uuid
from app.integrations.home_assistant import execute_ha_action
import asyncio

router = APIRouter()

@router.get("/health", tags=["Health"])
def health_check():
    """
    Healthcheck básico para verificar que el servidor está corriendo.
    
    Returns:
        dict: {"status": "ok"}
    """
    return {"status": "ok"}

@router.post("/mcp/order", response_model=MCPResult, tags=["MCP"])
def receive_mcp_order(payload: dict = Body(...)):
    """
    Recibe una orden MCP, valida el payload con Pydantic y JSON Schema,
    y responde con MCPResult. Si el intent es soportado por Home Assistant,
    ejecuta la acción real y devuelve el resultado.

    Request example:
        {
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
    Response example (success):
        {
            "status": "success",
            "action": "turn_off",
            "target": "light.king_s_bedroom",
            "message": "Order 'turn_off' for 'light.king_s_bedroom' executed via Home Assistant.",
            "version": "1.0.0",
            "request_id": "...",
            "timestamp": "..."
        }
    Response example (error):
        {
            "status": "error",
            "action": null,
            "target": null,
            "message": "Pydantic validation error: ...",
            "error_code": "pydantic_error"
        }
    """
    try:
        # Validación Pydantic (tipado rápido)
        order = MCPOrder(**payload)
    except PydanticValidationError as e:
        return JSONResponse(status_code=422, content={"status": "error", "action": None, "target": None, "message": f"Pydantic validation error: {e.errors()}", "error_code": "pydantic_error"})
    try:
        # Validación estricta con JSON Schema
        validate_mcp_order_jsonschema(payload)
    except JSONSchemaValidationError as e:
        return JSONResponse(status_code=422, content={"status": "error", "action": None, "target": None, "message": str(e), "error_code": "jsonschema_error"})
    # Ejecutar acción real en Home Assistant
    ha_result = asyncio.run(execute_ha_action(order.intent, order.target, order.context.dict() if order.context else {}))
    if ha_result["status"] == "success":
        result = MCPResult(
            status="success",
            action=order.intent,
            target=order.target,
            message=f"Order '{order.intent}' for '{order.target}' executed via Home Assistant.",
            version=order.version or "1.0.0",
            request_id=str(uuid.uuid4()),
            timestamp=datetime.datetime.utcnow().isoformat()
        )
        return result
    else:
        return JSONResponse(status_code=502, content={
            "status": "error",
            "action": order.intent,
            "target": order.target,
            "message": ha_result.get("message", "Unknown error from Home Assistant"),
            "error_code": ha_result.get("error_code", "ha_error")
        })

def include_routes(app: FastAPI):
    """
    Registra los endpoints principales en la app FastAPI.
    Args:
        app (FastAPI): Instancia principal de la aplicación.
    """
    app.include_router(router)
