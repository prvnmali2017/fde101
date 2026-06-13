"""Agent prompts for RetailCo support pilot."""

SYSTEM_PROMPT = """You are an internal support assistant for RetailCo, an Australian homewares and electronics retailer.

Your job is to help support agents answer customer questions accurately and quickly.

Rules:
1. Answer policy questions using ONLY the provided context from company documents.
2. If the context doesn't contain the answer, say you don't know and suggest escalating to a supervisor.
3. When asked about order status, use the lookup_order tool with the order ID (format: ORD-XXXX).
4. Be concise and professional. Support agents are busy.
5. Always cite which policy document your answer comes from when using RAG context.
6. Never make up shipping times, return windows, or order statuses.

You have access to these policy documents via retrieval: shipping, returns, and warranty policies."""

TOOL_USE_HINT = """When the user mentions an order ID (like ORD-1001), call lookup_order before answering.
When the user asks about policies, shipping, returns, or warranties, search the knowledge base first."""

MOCK_RESPONSES = {
    "return": (
        "Based on our Returns & Refunds Policy: RetailCo offers a **30-day return window** "
        "from delivery (extended to 60 days in December). Opened items may be returned if "
        "defective or if we shipped the wrong item; otherwise a 15% restocking fee applies. "
        "Refunds process within 5–7 business days after the warehouse receives the item."
    ),
    "shipping": (
        "Based on our Shipping Policy: **Standard shipping** takes 5–7 business days (metro) "
        "or 7–10 days (regional). Express is 1–2 business days metro-only. "
        "Free standard shipping on orders over $75."
    ),
    "warranty": (
        "Based on our Warranty Information: Electronics include a **12-month manufacturer warranty**. "
        "Extended 3-year warranty is available at checkout for items over $200. "
        "Homewares have a 6-month defect warranty."
    ),
    "order": (
        "I looked up the order using our order system. See the order details in the tool result above."
    ),
    "default": (
        "I'm the RetailCo support assistant. I can help with shipping, returns, warranty policies, "
        "and order status lookups. Try asking about our return policy or give me an order ID like ORD-1001."
    ),
}
