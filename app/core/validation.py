import json
from jsonschema import validate, ValidationError, Draft7Validator
from pathlib import Path

SCHEMA_PATH = Path(__file__).parent.parent / "schemas" / "mcp_order.schema.json"

with open(SCHEMA_PATH, encoding="utf-8") as f:
    MCP_ORDER_SCHEMA = json.load(f)

def validate_mcp_order_jsonschema(order_dict: dict) -> None:
    """
    Valida un dict de orden MCP contra el schema JSON oficial.
    Lanza ValidationError si no cumple el schema.
    """
    validator = Draft7Validator(MCP_ORDER_SCHEMA)
    errors = sorted(validator.iter_errors(order_dict), key=lambda e: e.path)
    if errors:
        msg = "; ".join([f"{'.'.join(map(str, e.path))}: {e.message}" for e in errors])
        raise ValidationError(f"MCPOrder JSON Schema validation failed: {msg}")
    # Si no hay errores, la orden es válida
