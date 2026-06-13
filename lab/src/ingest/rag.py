"""Document ingestion into ChromaDB for RAG."""

from __future__ import annotations

import os
from pathlib import Path

import chromadb
from chromadb.config import Settings

LAB_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = LAB_ROOT / "data" / "docs"

# Keep model cache inside the project (works in sandboxed/restricted environments)
_cache_root = LAB_ROOT / "data" / "cache"
os.environ.setdefault("XDG_CACHE_HOME", str(_cache_root))
os.environ.setdefault("CHROMA_CACHE_DIR", str(LAB_ROOT / "data" / "chroma-cache"))
COLLECTION_NAME = "retailco_policies"


def _chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks: list[str] = []
    current = ""

    for para in paragraphs:
        if len(current) + len(para) < chunk_size:
            current = f"{current}\n\n{para}".strip()
        else:
            if current:
                chunks.append(current)
            current = para

    if current:
        chunks.append(current)

    if not chunks:
        return [text[i : i + chunk_size] for i in range(0, len(text), chunk_size - overlap)]

    return chunks


def get_chroma_client() -> chromadb.ClientAPI:
    persist_dir = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma")
    Path(persist_dir).mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(
        path=persist_dir,
        settings=Settings(anonymized_telemetry=False),
    )


def ingest_documents(docs_dir: Path | None = None) -> int:
    """Ingest markdown docs into ChromaDB. Returns number of chunks indexed."""
    docs_dir = docs_dir or DOCS_DIR
    client = get_chroma_client()

    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(name=COLLECTION_NAME)
    total = 0

    for doc_path in sorted(docs_dir.glob("*.md")):
        text = doc_path.read_text(encoding="utf-8")
        chunks = _chunk_text(text)
        ids = [f"{doc_path.stem}-{i}" for i in range(len(chunks))]
        metadatas = [{"source": doc_path.name, "chunk": i} for i in range(len(chunks))]
        collection.add(documents=chunks, ids=ids, metadatas=metadatas)
        total += len(chunks)
        print(f"  Indexed {len(chunks)} chunks from {doc_path.name}")

    return total


def search_documents(query: str, n_results: int = 3) -> list[dict]:
    """Retrieve relevant document chunks for a query."""
    client = get_chroma_client()
    collection = client.get_collection(COLLECTION_NAME)
    results = collection.query(query_texts=[query], n_results=n_results)

    chunks = []
    for i, doc in enumerate(results["documents"][0]):
        meta = results["metadatas"][0][i]
        distance = results["distances"][0][i] if results.get("distances") else None
        chunks.append({"text": doc, "source": meta.get("source"), "score": distance})
    return chunks


if __name__ == "__main__":
    print(f"Ingesting documents from {DOCS_DIR}...")
    count = ingest_documents()
    print(f"Done. Indexed {count} chunks.")
