# Esquemas JSON para MCP (Model Context Protocol)

Este directorio contiene los esquemas JSON principales para el protocolo MCP, orientado a la integración de LLMs con Home Assistant y otros servicios.

## Archivos
- `mcp_order.schema.json`: Define la estructura de una orden MCP enviada al servidor.
- `mcp_result.schema.json`: Define la estructura de la respuesta/resultados de la ejecución de una orden MCP.

---

## 1. MCPOrder

### Propósito
Estandariza cómo se describe una orden para Home Assistant (o servicios compatibles), asegurando interoperabilidad y validación robusta.

### Estructura principal
- `user` (string, requerido): Identificador del usuario que envía la orden.
- `intent` (string, requerido): Acción a ejecutar (ej: `turn_on`, `play_media`, etc.).
- `target` (string, requerido): Entidad objetivo (formato: `domain.entity_id`, ej: `light.king_s_bedroom`).
- `context` (objeto, opcional): Información contextual (área, ubicación, hora, etc.).
- `version` (string, opcional): Versión del schema MCPOrder.

#### Ejemplo
```json
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
```

---

## 2. MCPResult

### Propósito
Estandariza la respuesta del servidor MCP tras ejecutar una orden, permitiendo trazabilidad, manejo de errores y feedback claro al usuario o sistema.

### Estructura principal
- `status` (string, requerido): `success` o `error`.
- `action` (string, requerido): Acción ejecutada (ej: `turn_off`).
- `target` (string, requerido): Entidad objetivo (formato: `domain.entity_id`).
- `message` (string, opcional): Mensaje descriptivo para el usuario.
- `error_code` (string, opcional): Código de error devuelto por Home Assistant (si aplica).
- `version` (string, opcional): Versión del schema MCPResult.
- `request_id` (string, opcional): Identificador único de la request.
- `timestamp` (string, opcional): Fecha y hora de la respuesta.

#### Ejemplo
```json
{
  "status": "success",
  "action": "turn_off",
  "target": "light.king_s_bedroom",
  "message": "The light in King's Bedroom has been turned off.",
  "version": "1.0.0",
  "request_id": "abc123",
  "timestamp": "2025-07-22T21:45:01"
}
```

---

## Recomendaciones de integración
- Valida todas las órdenes entrantes y salientes usando estos schemas para robustez y seguridad.
- Usa el campo `version` para facilitar migraciones y compatibilidad futura.
- Extiende los schemas agregando nuevos intents, áreas o metadatos según crezcan tus necesidades.
- Consulta la [documentación oficial de servicios de Home Assistant](https://www.home-assistant.io/integrations/#services) para mantener la lista de intents y targets actualizada.

---

¿Dudas o sugerencias? ¡Edita este README o abre un issue en el repo! 