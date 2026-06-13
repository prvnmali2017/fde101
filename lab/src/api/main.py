"""FastAPI application for RetailCo support pilot."""

from __future__ import annotations

from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from src.agent.support_agent import chat

load_dotenv()

app = FastAPI(
    title="RetailCo Support AI Pilot",
    description="Forward Deployed Engineer lab — RAG + order lookup for support agents",
    version="0.1.0",
)

STATIC_DIR = Path(__file__).resolve().parents[1] / "static"
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, examples=["What is the return policy?"])
    history: list[dict] = Field(default_factory=list)


class ChatResponse(BaseModel):
    reply: str
    sources: list[str]
    tool_calls: list[dict]
    mode: str


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


@app.get("/", include_in_schema=False)
async def root():
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/health", response_model=HealthResponse)
async def health():
    return HealthResponse(status="ok", service="retailco-support-pilot", version="0.1.0")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    result = chat(request.message, request.history)
    return ChatResponse(**result)


@app.get("/docs-info", include_in_schema=False)
async def docs_info():
    """List indexed policy documents."""
    docs_dir = Path(__file__).resolve().parents[2] / "data" / "docs"
    docs = [f.name for f in sorted(docs_dir.glob("*.md"))]
    return {"documents": docs, "count": len(docs)}
