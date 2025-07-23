# 🧠 MCP (Model Context Protocol) para LLM + Home Assistant

## ✨ Visión

Inspirados en el [repo oficial de Model Context Protocol](https://github.com/modelcontextprotocol/servers), construiremos un **protocolo estándar (MCP)** para que cualquier LLM (GPT, Claude, Ollama, etc.) pueda recibir contexto estructurado, interpretar órdenes y ejecutarlas sobre Home Assistant (y potencialmente otros servicios) de forma consistente, segura y agnóstica del proveedor del modelo.

---

## 🎯 Objetivo

* Que cualquier LLM pueda interactuar con un servidor MCP.
* Que el MCP reciba las respuestas del LLM en un formato bien definido (JSON MCP), las valide y ejecute sobre servicios reales (por ahora: Home Assistant).
* Mantenerlo modular para añadir más servicios en el futuro (Tasker, Telegram, Spotify, etc.).
* Garantizar interoperabilidad gracias a un schema inspirado en las buenas prácticas del repo oficial de MCP.

---

## 🏗️ Cómo lo vamos a lograr

### 📄 Componentes principales

1. **MCP Schema**: Especificación clara en JSON Schema de cómo se ve una orden MCP (inputs y outputs), alineada con el repositorio MCP oficial.
2. **Servidor MCP**: Una API ligera (FastAPI, Flask, Express) que recibe las órdenes MCP, valida contra el schema y ejecuta las acciones.
3. **Integración con Home Assistant**: Llama a la REST API de HA con el token y ejecuta las acciones.
4. **Prompts para LLM**: Diseñar instrucciones para que los LLM respondan en formato MCP.
5. **Pruebas y validación**: Garantizar que la comunicación LLM → MCP → Home Assistant funcione correctamente.
6. **Intents documentados**: Basarse en los servicios disponibles de Home Assistant para definir los intents posibles (encender/apagar, ajustar brillo, reproducir, pausar, limpiar, etc.).

---

## 📋 Dispositivos actuales para integrar

Revisados y verificados con la [documentación oficial de servicios de Home Assistant](https://www.home-assistant.io/integrations/#services), los posibles **intents** y entidades disponibles son:

* 💡 **Lámparas Philips Hue** → ✅ `light.turn_on`, ✅ `light.turn_off`, ✅ `light.turn_on` con atributos `brightness`, `color_name`, `hs_color`.
* 📺 **Samsung Smart TV** → ✅ `media_player.turn_on`, ✅ `media_player.turn_off`, ✅ `media_player.play_media`, ✅ `media_player.volume_set`, ✅ `media_player.select_source`.
* 🤖 **Aspiradora Roborock** → ✅ `vacuum.start`, ✅ `vacuum.stop`, ✅ `vacuum.return_to_base`, ✅ `vacuum.set_fan_speed`, y opcionalmente `vacuum.clean_spot`, `vacuum.pause`.
* 📡 **Google Chromecast** → ✅ `media_player.play_media`, ✅ `media_player.stop`, ✅ `media_player.pause`, ✅ `media_player.volume_set`, y `media_player.media_next_track`, `media_player.media_previous_track`.
* 🔊 **Philips Soundbar** → ✅ `media_player.turn_on`, ✅ `media_player.turn_off`, ✅ `media_player.volume_set`, ✅ `media_player.select_source`.
* 🏠 **Google Home** → ✅ `notify` para TTS (text-to-speech), o como `media_player` con los mismos servicios de Chromecast.
* 🎵 **Amazon Echo Dot con Alexa** → ✅ a través de la integración oficial de Alexa (requiere configuración), o también como `media_player` con comandos limitados (`turn_on`, `turn_off`, `volume_set`, etc.).

Estos servicios están validados y son los oficiales para las entidades correspondientes en Home Assistant.

---

## 📋 Roadmap de tareas

### 🧭 Fase 1: Diseño conceptual

* [ ] Definir objetivo principal (por ahora: Home Assistant)
* [ ] Definir entidades y conceptos clave: `user`, `intent`, `target`, `context`, `status`, etc., inspirados en las estructuras del repo MCP.
* [ ] Elegir formato de comunicación: JSON.
* [ ] Redactar un primer `mcp.schema.json` alineado a las mejores prácticas encontradas en el repo MCP.
* [ ] Documentar los intents disponibles para los dispositivos actuales.

### 🧪 Fase 2: Validación técnica

* [ ] Montar un servidor básico MCP (FastAPI recomendado).
* [ ] Implementar validador de MCP usando JSON Schema.
* [ ] Implementar la primera acción: encender/apagar una luz en Home Assistant.
* [ ] Probar flujo completo:

  * Input: MCP → MCP ejecuta en HA → Output: MCP con `status`.

### 🤖 Fase 3: Integración con LLM

* [ ] Diseñar prompts para LLM para que respondan en formato MCP.
* [ ] Probar con GPT-4 / Claude / AnythingLLM.
* [ ] Ajustar schema y ejemplos hasta lograr consistencia.

### 🌟 Fase 4: Extensiones y mejoras

* [ ] Soportar más servicios (Tasker, Telegram, Spotify, etc.).
* [ ] Agregar autenticación y control de acceso.
* [ ] Agregar memoria/contexto para conversaciones más naturales.
* [ ] Documentar todo y (opcional) publicar como proyecto open-source.

---

## 📄 Ejemplo de orden MCP

### Input

```json
{
  "user": "lucas",
  "intent": "turn_off",
  "target": "light.king_s_bedroom",
  "context": {
    "location": "home",
    "time": "2025-07-22T21:45:00"
  }
}
```

### Output

```json
{
  "status": "success",
  "action": "light.turn_off",
  "target": "light.king_s_bedroom",
  "message": "The light in King’s Bedroom has been turned off."
}
```

---

## 📌 Próximos pasos

✅ Elegir stack para el servidor (propuesto: FastAPI + Pydantic).
✅ Redactar MCP schema v0.1, referenciando ejemplos del repo oficial.
✅ Crear el repo y poner este README como base.
✅ Avanzar con la Fase 1.1 y 1.2 juntos.
✅ Documentar intents compatibles con tus dispositivos (ya verificados).

---

👊 Cuando quieras, arrancamos con la Fase 1.1 y definimos las entidades y el primer draft del schema, aprovechando también las ideas del [repo MCP](https://github.com/modelcontextprotocol/servers) y la documentación oficial de Home Assistant. ¡Listo para avanzar cuando vos digas! 🚀
