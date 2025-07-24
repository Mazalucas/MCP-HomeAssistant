"""
Integración con Home Assistant (HA) para el MCP Server.

- Gestiona la comunicación con la REST API de Home Assistant.
- Autenticación mediante token Bearer.
- Expone funciones para ejecutar intents (turn_on, turn_off, etc.).
- Traduce respuestas/errores de HA a MCPResult.

Configuración:
    - HOME_ASSISTANT_TOKEN: Token de acceso (Bearer) en variable de entorno o .env.
    - HOME_ASSISTANT_URL: URL base de la API de HA (ej: http://localhost:8123/api) en variable de entorno o .env.

Dependencias:
    - httpx (asíncrono)
    - python-dotenv (opcional, para cargar .env automáticamente)

Al importar este módulo, se cargan automáticamente las variables de entorno desde un archivo .env si existe.

Nota:
    El payload enviado a Home Assistant solo incluye 'entity_id'.
    El campo 'context' de la orden MCP NO se mezcla en el request a HA.

Ejemplo de uso:
    from app.integrations.home_assistant import execute_ha_action
    result = await execute_ha_action("turn_on", "light.living_room", {}, token, base_url)
"""
import os
from dotenv import load_dotenv
import httpx
from typing import Any, Dict

# Cargar variables de entorno desde .env automáticamente
load_dotenv()

HOME_ASSISTANT_TOKEN = os.getenv("HOME_ASSISTANT_TOKEN", "")
HOME_ASSISTANT_URL = os.getenv("HOME_ASSISTANT_URL", "http://localhost:8123/api")

async def execute_ha_action(intent: str, target: str, context: dict = None, token: str = None, base_url: str = None) -> Dict[str, Any]:
    """
    Ejecuta una acción en Home Assistant usando la REST API.

    Args:
        intent (str): Acción/intención a ejecutar (ej: turn_on, turn_off).
        target (str): Entidad objetivo (ej: light.living_room).
        context (dict, opcional): Contexto adicional para la acción (NO se envía a HA).
        token (str, opcional): Token Bearer de HA. Si no se pasa, usa variable de entorno.
        base_url (str, opcional): URL base de HA. Si no se pasa, usa variable de entorno.

    Returns:
        dict: Respuesta de la API de HA (éxito o error).
    """
    token = token or HOME_ASSISTANT_TOKEN
    base_url = base_url or HOME_ASSISTANT_URL
    if not token or not base_url:
        return {"status": "error", "error_code": "config_error", "message": "Falta token o URL de Home Assistant"}
    # Mapear intent a endpoint y payload de HA
    domain, _ = target.split(".", 1)
    service = intent  # Ej: "turn_on"
    url = f"{base_url}/services/{domain}/{service}"
    payload = {"entity_id": target}  # Solo entity_id, no mezclar context
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.post(url, json=payload, headers=headers, timeout=10)
            if resp.status_code == 200:
                return {"status": "success", "data": resp.json()}
            else:
                return {"status": "error", "error_code": f"ha_{resp.status_code}", "message": resp.text}
        except Exception as e:
            return {"status": "error", "error_code": "ha_exception", "message": str(e)}
