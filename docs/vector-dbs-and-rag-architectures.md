# Vector Databases & RAG Architectures

A practical reference for Forward Deployed Engineers — how retrieval works, which vector store to pick, and common RAG patterns you'll deploy at customer sites.

**Related:** The RetailCo lab uses the simplest pattern (Naive RAG + ChromaDB). See `../lab/src/ingest/rag.py`.

---

## Part 1 — How RAG Works

**RAG (Retrieval-Augmented Generation)** grounds LLM answers in external data instead of relying on model memory alone.

```
Documents → Ingestion (chunk + embed) → Vector DB
User query → embed → similarity search → prompt + chunks → LLM → grounded answer
```

### Core concepts

| Term | Meaning |
|------|---------|
| **Embedding** | A dense vector (e.g. 384–1536 floats) representing semantic meaning of text |
| **Chunk** | A slice of a document fed to the retriever (typical: 256–1024 tokens) |
| **Similarity search** | Find chunks whose embeddings are closest to the query (cosine, dot product, L2) |
| **Top-k** | Number of chunks retrieved per query (usually 3–10) |
| **Metadata filter** | Restrict search by tenant, doc type, date, ACL — critical in enterprise |
| **Reranker** | Second-stage model that re-scores retrieved chunks for relevance |

### The ingestion pipeline

1. **Load** — read from files, S3, Confluence, SharePoint, databases
2. **Parse** — extract text (and tables/images for advanced setups)
3. **Chunk** — split into retrievable units with overlap
4. **Embed** — call an embedding model (OpenAI, Bedrock Titan, local sentence-transformers)
5. **Store** — upsert vectors + metadata + original text into the vector DB
6. **Index** — build ANN (approximate nearest neighbor) index for fast search

Your lab implements steps 3–5 in `../lab/src/ingest/rag.py`.

---

## Part 2 — Vector Database Landscape

| Database | Type | Best for | AWS fit | Hybrid search |
|----------|------|----------|---------|---------------|
| **ChromaDB** | Embedded/server | Local dev, pilots | Run on ECS/EC2 | Limited |
| **pgvector** | Postgres extension | Teams on Postgres | RDS / Aurora | Via full-text |
| **OpenSearch** | Search + k-NN | AWS-native enterprise | Native | Native (BM25 + k-NN) |
| **Amazon Bedrock KB** | Managed RAG | Fastest AWS pilot | Native | Automatic |
| **Pinecone** | Vector DB SaaS | Fast time-to-market | VPC peering | Sparse-dense |
| **Weaviate** | Vector-native | Multi-modal | EKS / SaaS | BM25 + vector |
| **Qdrant** | Vector-native | Self-host, filtering | EKS / EC2 | Sparse vectors |
| **Milvus / Zilliz** | Distributed | 100M+ vectors | EKS | Hybrid |
| **Azure AI Search** | Search + vector | Azure enterprise | (Azure) | Native + semantic ranker |
| **Vertex AI Vector Search** | Managed ANN | GCP scale | (GCP) | Via hybrid |

### Quick profiles

- **ChromaDB** — lightweight, Python-first; perfect for 2-week pilots (your lab). Not for multi-tenant scale.
- **pgvector** — vectors alongside relational data; great when "we can't add another database."
- **OpenSearch** — BM25 + vector hybrid, IAM/VPC; the AWS production upgrade from Chroma.
- **Bedrock KB / Azure "on your data" / Vertex RAG Engine** — managed RAG; fastest path, less control.
- **Pinecone** — simple managed SaaS; data may leave VPC unless Enterprise.

---

## Part 3 — Decision Guide for FDE Pilots

```
Where must the data live?
├─ "In our AWS"      → OpenSearch Serverless / Bedrock KB (managed) / Aurora pgvector
├─ "In our Azure"    → Azure AI Search / Cosmos DB for PostgreSQL (pgvector)
├─ "In our GCP"      → Vertex AI Vector Search / AlloyDB pgvector
├─ "SaaS is fine"    → Pinecone / Weaviate Cloud
└─ "Local POC only"  → ChromaDB (your lab) → plan migration before demo day
```

### Pilot → production arc

| Phase | Store | Why |
|-------|-------|-----|
| Week 1–2 pilot | ChromaDB or managed KB | Speed |
| Production v1 | OpenSearch / pgvector / AI Search | Customer VPC, IAM, audit |
| Scale-out | OpenSearch cluster / Milvus | Volume / latency SLAs |

---

## Part 4 — RAG Architecture Patterns

### 1. Naive RAG (baseline)
Query → embed → top-k retrieve → stuff context → LLM. Simple, great for FAQ/policy docs. **Your lab uses this.**

### 2. Hybrid RAG (keyword + vector)
Run BM25 and vector search, merge, rerank. Handles exact IDs/SKUs/error codes. Use OpenSearch, AI Search, Weaviate, Qdrant.

### 3. Agentic RAG
LLM decides *when* to retrieve and *what* to query, and can call tools/APIs. Matches real support workflows (your lab's order lookup is a step toward this; aiops-develop MCP work is full agentic).

### 4. Graph RAG
Extract entities/relationships into a knowledge graph; traverse + vector search. Multi-hop questions (supply chain, legal, finance). Neo4j, Neptune, Microsoft GraphRAG.

### 5. Multi-vector / Multi-modal RAG
Different embeddings per content type (text, tables, images). Manuals, financial reports, scanned PDFs. Unstructured.io, LlamaParse, ColPali.

### 6. RAG with reranking
Retrieve top-20 → cross-encoder reranker → keep top-3 → LLM. Big quality boost. Cohere Rerank, Bedrock Rerank, bge-reranker.

### 7. Corrective / Self-RAG (CRAG)
LLM grades retrieved chunks; if irrelevant, rewrite query or fall back to web/API. High-stakes domains.

---

## Part 5 — Patterns by Customer Scenario

| Scenario | Pattern | Vector DB |
|----------|---------|-----------|
| Internal support FAQ (RetailCo) | Naive RAG + tools | ChromaDB → OpenSearch |
| Enterprise AWS, security-sensitive | Bedrock KB or OpenSearch + Bedrock embeddings | OpenSearch Serverless |
| Already on Postgres | Naive RAG + SQL tools | pgvector |
| E-commerce + order APIs | Agentic RAG + hybrid | OpenSearch / Pinecone |
| Legal / compliance | RAG + reranking + citations | OpenSearch |
| Multi-tenant SaaS | Namespaced vectors + metadata ACL | Pinecone / pgvector RLS |
| Observability / SRE assistant | Agentic RAG + MCP tools | Existing (Splunk, NR) |

---

## Part 6 — Chunking & Embedding Choices

### Chunking
| Strategy | Size | Best for |
|----------|------|----------|
| Fixed token window | 256–512, 10–20% overlap | General |
| Paragraph/section | Variable | Policy docs (your lab) |
| Semantic | LLM topic boundaries | Long unstructured docs |
| Parent-child | Small for search, large for context | Better answers |

### Embedding models
| Model | Dims | Provider |
|-------|------|----------|
| text-embedding-3-small | 1536 | OpenAI |
| amazon.titan-embed-text-v2 | 1024 | Bedrock |
| all-MiniLM-L6-v2 | 384 | Local / Chroma default |
| cohere.embed-english-v3 | 1024 | Cohere |
| Azure OpenAI text-embedding-3 | 1536 | Azure |
| Vertex text-embedding-004 | 768 | GCP |

**Rule:** match embedding model at ingest and query time. Re-embed everything if you change models.

---

## Part 7 — Evaluation

| Metric | Measures | Tool |
|--------|----------|------|
| Retrieval recall@k | Right chunk in top-k? | Custom, RAGAS |
| Answer faithfulness | Grounded in context? | RAGAS, LLM-as-judge |
| Answer relevance | Answers the question? | Human eval, RAGAS |
| Latency p95 | End-to-end time | CloudWatch, Prometheus |
| Citation accuracy | Sources correct? | Manual review |

**Pilot target (RetailCo):** 80% on a 15-question eval set.

```python
test_cases = [
    {"question": "What is the return policy?", "must_contain": ["30 day", "30-day"]},
    {"question": "Status of ORD-1001?", "must_contain": ["Delivered"]},
]
```

---

## Quick Reference Card

```
NAIVE RAG    = embed + search + prompt        → pilots, FAQs
HYBRID RAG   = BM25 + vector + merge          → enterprise search
AGENTIC RAG  = LLM chooses tools + retrieval  → support, ops, APIs
RERANKING    = retrieve many, keep best few    → production quality
BEDROCK KB   = managed, AWS-native             → fast AWS pilots
OPENSEARCH   = hybrid, IAM, VPC                → AWS production
PGVECTOR     = Postgres-native                 → minimal new infra
CHROMADB     = local / dev                     → your lab today
```
