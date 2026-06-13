"""Support agent — RAG + tool use."""

from __future__ import annotations

import json
import os

from openai import OpenAI

from src.agent.prompts import MOCK_RESPONSES, SYSTEM_PROMPT, TOOL_USE_HINT
from src.agent.tools import TOOL_DEFINITIONS, extract_order_id, lookup_order
from src.ingest.rag import search_documents


def _mock_response(message: str, order_result: dict | None) -> str:
    lower = message.lower()
    if order_result and order_result.get("found"):
        o = order_result
        tracking = f" Tracking: {o['tracking']}." if o.get("tracking") else ""
        delivered = f" Delivered: {o['delivered_at']}." if o.get("delivered_at") else ""
        return (
            f"**Order {o['order_id']}** — Status: **{o['status']}**. "
            f"Items: {', '.join(o['items'])}.{tracking}{delivered}"
        )
    if any(w in lower for w in ("return", "refund", "exchange")):
        return MOCK_RESPONSES["return"]
    if any(w in lower for w in ("ship", "delivery", "tracking")):
        return MOCK_RESPONSES["shipping"]
    if any(w in lower for w in ("warranty", "defect", "broken")):
        return MOCK_RESPONSES["warranty"]
    if extract_order_id(message):
        o = lookup_order(extract_order_id(message) or "")
        if o.get("found"):
            return _mock_response(message, o)
        return f"Order {o['order_id']} was not found in the system."
    return MOCK_RESPONSES["default"]


def _format_context(chunks: list[dict]) -> str:
    if not chunks:
        return "No relevant documents found."
    parts = []
    for c in chunks:
        parts.append(f"[Source: {c['source']}]\n{c['text']}")
    return "\n\n---\n\n".join(parts)


def _run_tool(name: str, arguments: str) -> dict:
    args = json.loads(arguments)
    if name == "lookup_order":
        return lookup_order(args["order_id"])
    return {"error": f"Unknown tool: {name}"}


def chat(message: str, conversation_history: list[dict] | None = None) -> dict:
    """
    Process a support agent message.
    Returns reply, sources used, and any tool calls made.
    """
    conversation_history = conversation_history or []
    order_id = extract_order_id(message)
    tool_results: list[dict] = []

    if order_id:
        result = lookup_order(order_id)
        tool_results.append({"tool": "lookup_order", "input": order_id, "output": result})

    chunks = search_documents(message, n_results=3)
    context = _format_context(chunks)
    sources = list({c["source"] for c in chunks if c.get("source")})

    mock_mode = os.getenv("MOCK_LLM", "true").lower() == "true"
    if mock_mode or not os.getenv("OPENAI_API_KEY"):
        order_result = tool_results[0]["output"] if tool_results else None
        reply = _mock_response(message, order_result)
        if chunks and not order_id:
            reply += f"\n\n_Sources: {', '.join(sources)}_"
        return {
            "reply": reply,
            "sources": sources,
            "tool_calls": tool_results,
            "mode": "mock",
        }

    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

    messages = [
        {"role": "system", "content": f"{SYSTEM_PROMPT}\n\n{TOOL_USE_HINT}"},
        *conversation_history,
        {
            "role": "user",
            "content": (
                f"Context from knowledge base:\n{context}\n\n"
                f"Agent question: {message}"
            ),
        },
    ]

    if tool_results:
        messages[-1]["content"] += (
            f"\n\nOrder lookup result (already fetched): {json.dumps(tool_results[0]['output'])}"
        )

    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
        temperature=0.2,
    )

    choice = response.choices[0]

    if choice.message.tool_calls:
        for tc in choice.message.tool_calls:
            result = _run_tool(tc.function.name, tc.function.arguments)
            tool_results.append(
                {
                    "tool": tc.function.name,
                    "input": json.loads(tc.function.arguments),
                    "output": result,
                }
            )

        messages.append(choice.message)
        for tc, tr in zip(choice.message.tool_calls, tool_results[-len(choice.message.tool_calls) :]):
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tc.id,
                    "content": json.dumps(tr["output"]),
                }
            )

        follow_up = client.chat.completions.create(model=model, messages=messages, temperature=0.2)
        reply = follow_up.choices[0].message.content or ""
    else:
        reply = choice.message.content or ""

    return {
        "reply": reply,
        "sources": sources,
        "tool_calls": tool_results,
        "mode": "openai",
    }
