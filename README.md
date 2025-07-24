# MCP Server para LLM + Home Assistant

## ✨ Descripción

Este proyecto implementa un **servidor MCP (Model Context Protocol)** en Python usando FastAPI, diseñado para servir de puente estándar entre modelos de lenguaje (LLMs como Claude, GPT, etc.) y Home Assistant (u otros servicios domóticos). Permite que cualquier LLM estructure órdenes en JSON, las valide y las ejecute sobre dispositivos reales, devolviendo resultados también estandarizados.

## 🎯 Objetivos
- Estandarizar la comunicación entre LLMs y sistemas domóticos.
- Permitir que cualquier modelo pueda autodescubrir cómo interactuar con el servidor (descubrimiento de schemas, entidades, atributos, ejemplos y prompts).
- Soportar integración real y segura con Home Assistant vía REST API y token.
- Facilitar la extensión a nuevos dispositivos y servicios.

## 🚀 Requisitos
- Python 3.10+
- Home Assistant corriendo y accesible desde el servidor MCP
- Token de acceso de Home Assistant (long-lived access token)

## 📦 Instalación y configuración

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/Mazalucas/MCP-HomeAssistant.git
   cd MCP-HomeAssistant
   ```

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   # O manualmente:
   pip install fastapi uvicorn httpx pydantic python-dotenv jsonschema pytest pytest-asyncio
   ```

3. **Configura las variables de entorno:**
   Crea un archivo `.env` en la raíz del proyecto con:
   ```env
   HOME_ASSISTANT_TOKEN=tu_token_largo_de_home_assistant
   HOME_ASSISTANT_URL=http://homeassistant.local:8123/api
   ```

4. **(Opcional) Exporta tus entidades de Home Assistant:**
   - Copia la tabla de entidades desde las herramientas de desarrollador de HA y pégala en un archivo llamado `Entidades-Actuales.md` en la raíz del proyecto.

5. **Lanza el servidor:**
   ```bash
   uvicorn app.main:app --reload
   ```
   El servidor estará disponible en `http://localhost:8000`.

## 🩺 Endpoints de salud y stats

- **Healthcheck:**
  - [GET /health](http://localhost:8000/health)
  - Responde `{ "status": "ok" }` si el servidor está corriendo.

- **Schema de orden MCP:**
  - [GET /mcp/schema/order](http://localhost:8000/mcp/schema/order)
  - Devuelve el JSON Schema de las órdenes válidas.

- **Schema de resultado MCP:**
  - [GET /mcp/schema/result](http://localhost:8000/mcp/schema/result)

- **Entidades y atributos soportados:**
  - [GET /mcp/entities](http://localhost:8000/mcp/entities)

- **Ejemplos de uso:**
  - [GET /mcp/examples](http://localhost:8000/mcp/examples)

- **Prompt de sistema para LLMs:**
  - [GET /mcp/prompt](http://localhost:8000/mcp/prompt)

## 🧑‍💻 Ejemplo de uso

1. **Prueba el healthcheck:**
   ```bash
   curl http://localhost:8000/health
   # Respuesta: { "status": "ok" }
   ```

2. **Envía una orden MCP:**
   ```bash
   curl -X POST http://localhost:8000/mcp/order \
     -H 'Content-Type: application/json' \
     -d '{
       "user": "lucas",
       "intent": "turn_on",
       "target": "light.living_room",
       "context": { "brightness": 200, "color_name": "blue" }
     }'
   ```

3. **Descubre entidades y atributos soportados:**
   ```bash
   curl http://localhost:8000/mcp/entities
   ```

4. **Obtén el prompt de sistema para LLMs:**
   ```bash
   curl http://localhost:8000/mcp/prompt
   ```

## 🤖 Integración con LLMs
- Usa el endpoint `/mcp/prompt` para obtener un prompt de sistema listo para Claude, GPT, etc.
- El LLM debe responder con un JSON válido según el schema de orden.
- Puedes usar el script `mcp_bridge.py` para pegar el JSON generado por el LLM y ejecutarlo sobre Home Assistant.

## 🛠️ Testing
- Ejecuta los tests con:
  ```bash
  pytest tests/test_endpoints.py
  ```

## 📚 Recursos útiles
- [Documentación oficial de Home Assistant](https://www.home-assistant.io/integrations/#services)
- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Anthropic Claude](https://www.anthropic.com/)
- [OpenAI GPT](https://platform.openai.com/docs/)

---

¿Dudas, sugerencias o quieres contribuir? ¡Abre un issue o PR en el repo! 

## 🔑 Configuración del archivo .env y API Key

Para que el MCP Server pueda comunicarse con tu Home Assistant, debes crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
HOME_ASSISTANT_TOKEN=tu_token_largo_de_home_assistant
HOME_ASSISTANT_URL=http://homeassistant.local:8123/api
```

- **HOME_ASSISTANT_TOKEN**: Es un "Long-Lived Access Token" de Home Assistant. Puedes generarlo desde tu perfil de usuario en la interfaz web de Home Assistant:
  1. Ve a tu usuario (abajo a la izquierda en la UI de HA).
  2. Baja hasta la sección "Long-Lived Access Tokens".
  3. Haz clic en "Create Token", ponle un nombre y copia el token generado.
  4. Pega ese token en el archivo `.env` como se muestra arriba.
- **HOME_ASSISTANT_URL**: Es la URL base de tu instancia de Home Assistant, normalmente termina en `/api`.

> ⚠️ **Advertencia de seguridad:**
> Nunca compartas tu token de Home Assistant públicamente ni lo subas a repositorios. El archivo `.env` está en el `.gitignore` por defecto. 