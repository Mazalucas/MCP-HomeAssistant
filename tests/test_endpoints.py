import sys
import os
import pytest
from fastapi.testclient import TestClient
import httpx
import pytest
from unittest.mock import patch, AsyncMock
from app.integrations import home_assistant

# Permitir imports relativos desde app/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_mcp_order_valid():
    payload = {
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
    response = client.post("/mcp/order", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["action"] == "turn_off"
    assert data["target"] == "light.king_s_bedroom"
    assert "request_id" in data
    assert "timestamp" in data

def test_mcp_order_missing_field():
    payload = {
        # Falta 'user'
        "intent": "turn_off",
        "target": "light.king_s_bedroom"
    }
    response = client.post("/mcp/order", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["error_code"] == "pydantic_error"

def test_mcp_order_invalid_schema():
    payload = {
        "user": "lucas",
        "intent": "invalid_intent",  # Valor no permitido por el schema
        "target": "light.king_s_bedroom"
    }
    response = client.post("/mcp/order", json=payload)
    assert response.status_code == 422
    data = response.json()
    assert data["status"] == "error"
    assert data["error_code"] == "jsonschema_error"

@pytest.mark.asyncio
def test_execute_ha_action_success(monkeypatch):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 200
            def json(self):
                return {"result": "ok"}
        return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    import asyncio
    result = asyncio.run(home_assistant.execute_ha_action("turn_on", "light.living_room", {}, "token", "http://mock:8123/api"))
    assert result["status"] == "success"
    assert "data" in result

@pytest.mark.asyncio
def test_execute_ha_action_auth_error(monkeypatch):
    async def mock_post(*args, **kwargs):
        class MockResponse:
            status_code = 401
            text = "Unauthorized"
            def json(self):
                return {"error": "unauthorized"}
        return MockResponse()
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    import asyncio
    result = asyncio.run(home_assistant.execute_ha_action("turn_on", "light.living_room", {}, "badtoken", "http://mock:8123/api"))
    assert result["status"] == "error"
    assert result["error_code"] == "ha_401"

@pytest.mark.asyncio
def test_execute_ha_action_network_error(monkeypatch):
    async def mock_post(*args, **kwargs):
        raise httpx.ConnectError("Network unreachable")
    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    import asyncio
    result = asyncio.run(home_assistant.execute_ha_action("turn_on", "light.living_room", {}, "token", "http://mock:8123/api"))
    assert result["status"] == "error"
    assert result["error_code"] == "ha_exception"
