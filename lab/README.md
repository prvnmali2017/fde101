# RetailCo AI Support Pilot — Lab

A hands-on Forward Deployed Engineer lab: deliver a 2-week customer AI pilot locally.

## What You'll Build

- **RAG pipeline** — ingest RetailCo FAQ/policy docs, answer support questions
- **Order lookup tool** — agent calls a mock order API (simulates customer integration)
- **FastAPI backend** — REST API with `/chat` and `/health`
- **Simple web UI** — chat interface at http://localhost:8000
- **FDE deliverables** — runbook, demo script, discovery notes

## Prerequisites

- Python 3.11+
- Docker (optional — for containerized run)
- OpenAI API key **OR** run in mock mode (no key needed for basic demo)

## Quick Start

```bash
cd lab

# 1. Configure
cp .env.example .env
# Edit .env — set OPENAI_API_KEY or leave MOCK_LLM=true

# 2. Setup (creates venv, installs deps, ingests docs)
chmod +x scripts/*.sh
./scripts/setup.sh

# 3. Run
source .venv/bin/activate
uvicorn src.api.main:app --reload --port 8000

# 4. Demo (in another terminal)
./scripts/demo.sh
```

Open http://localhost:8000 for the chat UI, or http://localhost:8000/docs for Swagger.

## Mock Mode (No API Key)

Set `MOCK_LLM=true` in `.env`. The agent uses keyword matching instead of an LLM — enough to demo the architecture and tool-use flow in interviews.

## Lab Structure

```
lab/
├── customer-brief.md       # Fictional customer scenario
├── docker-compose.yml      # Containerized deployment
├── data/
│   ├── docs/               # RetailCo policy documents (RAG source)
│   └── orders.json         # Mock order database
├── deliverables/           # What you present to the customer
├── scripts/
│   ├── setup.sh
│   └── demo.sh
└── src/
    ├── api/                # FastAPI application
    ├── agent/              # Agent + tools + prompts
    └── ingest/             # Document ingestion → ChromaDB
```

## Exercises (FDE Practice)

### Exercise 1 — Discovery
Fill out `../templates/discovery-call-template.md` using `customer-brief.md`.

### Exercise 2 — Improve RAG
Add a new policy doc to `data/docs/`, re-run setup, verify the agent answers correctly.

### Exercise 3 — Real Integration
Replace `data/orders.json` lookup with a real HTTP call (see `src/agent/tools.py`).

### Exercise 4 — Deploy
Run `docker compose up --build` and complete `deliverables/deployment-runbook.md`.

### Exercise 5 — Demo
Follow `deliverables/demo-script.md` and record a 5-minute walkthrough.

## Evaluation Test Set

| Question | Expected behavior |
|----------|-------------------|
| "What is your return policy?" | Cites 30-day return window from docs |
| "How long does standard shipping take?" | 5–7 business days |
| "What's the status of order ORD-1001?" | Tool call → Delivered |
| "Can I return a opened item?" | References opened-item policy |

## Docker

```bash
docker compose up --build
```

API available at http://localhost:8000.

## Next Steps (Stretch)

- Add OpenTelemetry metrics (your SRE strength)
- Deploy to ECS with Terraform
- Swap ChromaDB for OpenSearch Serverless
- Add Bedrock as LLM provider
