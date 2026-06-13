"""Agent tools — simulates integration with customer systems."""

from __future__ import annotations

import json
import re
from pathlib import Path

ORDERS_FILE = Path(__file__).resolve().parents[2] / "data" / "orders.json"
ORDER_ID_PATTERN = re.compile(r"ORD-\d{4}", re.IGNORECASE)


def _load_orders() -> list[dict]:
    return json.loads(ORDERS_FILE.read_text(encoding="utf-8"))


def lookup_order(order_id: str) -> dict:
    """
    Look up order status by order ID.
    In production, this would call RetailCo's order API:
      GET https://api.retailco.com.au/v1/orders/{order_id}
      Authorization: Bearer <customer_api_key>
    """
    order_id = order_id.upper()
    for order in _load_orders():
        if order["order_id"] == order_id:
            return {
                "found": True,
                "order_id": order["order_id"],
                "status": order["status"],
                "items": order["items"],
                "tracking": order.get("tracking"),
                "ordered_at": order["ordered_at"],
                "delivered_at": order.get("delivered_at"),
            }
    return {"found": False, "order_id": order_id, "message": "Order not found in system."}


def extract_order_id(text: str) -> str | None:
    match = ORDER_ID_PATTERN.search(text)
    return match.group(0).upper() if match else None


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "lookup_order",
            "description": "Look up the status and details of a customer order by order ID (e.g. ORD-1001).",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "string",
                        "description": "The order ID, format ORD-XXXX",
                    }
                },
                "required": ["order_id"],
            },
        },
    }
]
