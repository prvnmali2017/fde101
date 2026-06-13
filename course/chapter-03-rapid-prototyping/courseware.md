# Chapter 3 — Rapid Prototyping & Customer Integration

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (build the API) + 1 exercise + quiz

---

## Chapter Overview

Now students build. This chapter teaches how to ship a working backend fast with FastAPI, structure a pilot codebase, and integrate a customer system — using the "mock first, integrate later" pattern. Students build the RetailCo API with a working order-lookup tool.

## Learning Objectives

By the end, students can:

1. Stand up a FastAPI service with clean, demoable endpoints
2. Structure an FDE pilot repo for speed and handoff
3. Apply the "mock first" integration pattern
4. Integrate a customer system (order lookup) behind a clean interface
5. Validate the build with a simple smoke test/demo script

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- Chapter 3: Rapid Prototyping & Integration
- "Ship the thinnest working thing"

**Speaker notes:** We're in the Build phase. Goal of this chapter: a running API the customer can poke at by the end.

---

### Slide 2 — The FDE build philosophy
- Working > perfect
- Demoable > complete
- Swappable > final

**Speaker notes:** Engineers over-build. FDEs ship a slice, demo it, iterate. Every component should be swappable (mock → real).

---

### Slide 3 — Tech stack for FDE pilots
- Python + FastAPI (fast, typed, auto-docs)
- Docker (deploy anywhere)
- A simple datastore (JSON/SQLite/Postgres)
- Optional: a thin HTML/React UI

**Speaker notes:** Justify FastAPI: auto Swagger docs = instant demo surface; Pydantic = fewer bugs; async-ready. Customers' IT teams can maintain Python.

---

### Slide 4 — Pilot repo structure
```
lab/
├── src/
│   ├── api/      # FastAPI app
│   ├── agent/    # logic + tools
│   └── ingest/   # data pipeline
├── data/         # docs + mock data
├── scripts/      # setup, demo
└── deliverables/ # runbook, demo script
```

**Speaker notes:** Walk the structure of `../lab/`. Separation of api/agent/ingest makes it easy to swap parts and hand off. `deliverables/` signals professionalism to customers.

---

### Slide 5 — Anatomy of a FastAPI app
- `app = FastAPI(...)`
- Pydantic models for request/response
- Endpoints: `/health`, `/chat`
- Auto docs at `/docs`

**Speaker notes:** Show `../lab/src/api/main.py`. Point out the typed `ChatRequest`/`ChatResponse` and the free Swagger UI — your instant demo tool.

---

### Slide 6 — Why /health matters first
- Proves the service is up
- First thing you wire in deployment
- Customers/monitoring depend on it

**Speaker notes:** SRE habit that pays off. A `/health` endpoint is the smallest deployable unit and your first deploy smoke test.

---

### Slide 7 — Request/response with Pydantic
- Validate input at the edge
- Self-documenting schemas
- Fewer runtime surprises

**Speaker notes:** Show the `ChatRequest` model with field constraints (min/max length). Validation = fewer demo-day crashes.

---

### Slide 8 — The "mock first" principle
- Customer access is always delayed
- Build against fake data shaped like the real thing
- Swap in the real integration later — no rewrite

**Speaker notes:** This is the chapter's key idea. RetailCo's order API isn't ready? Use `data/orders.json` shaped exactly like the API response. Build now, integrate later.

---

### Slide 9 — Integration behind an interface
- One function = one integration point
- `lookup_order(order_id)` hides the source
- Today: JSON file. Tomorrow: HTTP call. Same signature.

**Speaker notes:** Show `../lab/src/agent/tools.py`. The `lookup_order` docstring even contains the real API call it will become. Callers never change.

---

### Slide 10 — Tool/function design
- Clear name + single responsibility
- Typed inputs, structured output
- Return `found: true/false`, not exceptions for "not found"

**Speaker notes:** Good tool design matters double in Ch 4 when an LLM calls these. Structured returns make both humans and models reliable.

---

### Slide 11 — Extracting structured data from messy input
- Customers paste free text ("status of ORD-1001?")
- Use regex/parsing to extract IDs
- `extract_order_id()` finds `ORD-\d{4}`

**Speaker notes:** Show the regex in `tools.py`. Real customer input is messy; a little parsing makes the pilot feel smart.

---

### Slide 12 — Configuration & secrets
- `.env` for config (never commit it)
- `.env.example` to document required vars
- Feature flags (e.g., `MOCK_LLM=true`)

**Speaker notes:** Show `../lab/.env.example`. The `MOCK_LLM` flag lets the pilot run with zero secrets — huge for demos and security reviews.

---

### Slide 13 — Running the service
- `uvicorn src.api.main:app --reload`
- Hit `/docs` to test interactively
- `/health` to confirm up

**Speaker notes:** Live: start the server, open Swagger, call `/chat`. Show the auto-generated docs as your demo surface.

---

### Slide 14 — A smoke test / demo script
- Automate the happy path
- `scripts/demo.sh` curls the key endpoints
- Run it before every customer demo

**Speaker notes:** Show `../lab/scripts/demo.sh`. Running this before a demo catches breakage. Customers see a confident, working flow.

---

### Slide 15 — Setup automation
- `scripts/setup.sh`: venv, deps, data ingest
- One command = reproducible environment
- Critical for handoff

**Speaker notes:** Walk `../lab/scripts/setup.sh`. A one-command setup means the customer's team can run it after you leave. Reproducibility = trust.

---

### Slide 16 — A minimal UI (optional but powerful)
- Single `index.html` chat page
- Talks to `/chat`
- Non-technical stakeholders need to SEE it

**Speaker notes:** Show `../lab/src/static/index.html`. Executives don't read JSON. A simple chat UI dramatically improves demo impact for low effort.

---

### Slide 17 — Keeping it swappable
- Datastore: JSON → SQLite → Postgres
- LLM: mock → OpenAI → Bedrock
- Vector store: Chroma → OpenSearch
- Same interfaces throughout

**Speaker notes:** Reinforce: design for swap. This is what makes pilot → production smooth (Ch 5). Tease that Ch 4 swaps in the AI brain.

---

### Slide 18 — What we built
- Running FastAPI service
- `/health` + `/chat`
- Order lookup tool (mocked, swappable)
- Demo + setup scripts
- Optional chat UI

**Speaker notes:** Recap. Students now have a working backend skeleton. Next chapter gives it a brain with RAG + agents.

---

## Demo (Instructor-led): Build the API

**Goal:** Go from empty folder to running, demoable API.

**Walkthrough script:**

1. Show the repo structure in `../lab/`.
2. Open `src/api/main.py` — explain FastAPI app, models, endpoints.
3. Open `src/agent/tools.py` — explain `lookup_order` (mock now, HTTP later) and `extract_order_id`.
4. Run setup:
   ```bash
   cd ../lab
   cp .env.example .env
   ./scripts/setup.sh
   source .venv/bin/activate
   uvicorn src.api.main:app --reload --port 8000
   ```
5. Open `http://localhost:8000/docs`, call `/health`, then `/chat` with `"status of ORD-1001?"`.
6. Run `./scripts/demo.sh` to show the automated happy path.
7. Open `http://localhost:8000` to show the chat UI.

**Takeaway:** A working, demoable pilot backend in under an hour — without any real customer access yet.

---

## Hands-On Exercise

**Title:** Add a new tool and endpoint

**Instructions for students:**
1. Add a new mock tool `lookup_tracking(tracking_number)` returning a fake status.
2. Wire it so `/chat` recognizes a tracking number in the message.
3. Add the tracking data to `data/orders.json`.
4. Verify via `/docs` and update `scripts/demo.sh` with a new test.

**Deliverable:** Working new tool + passing demo script.

**Solution notes (instructor):** Look for: a clean single-responsibility function, structured return, and a regex/extraction step. Bonus if they keep it swappable (docstring noting the real API).

---

## Quiz (5 questions)

1. What does "mock first" mean and why use it? *(build against fake data shaped like real; unblocks before access granted)*
2. Why expose a `/health` endpoint first? *(deploy smoke test; monitoring; smallest deployable unit)*
3. How does hiding an integration behind a function help later? *(swap source without changing callers)*
4. Why return `found: false` instead of throwing for "not found"? *(structured, predictable for humans and LLMs)*
5. Why add a simple UI for a backend pilot? *(non-technical stakeholders need to see it to buy in)*

---

## Downloadable Resources

- Lab code → `../lab/src/`
- Setup & demo scripts → `../lab/scripts/`
- Env template → `../lab/.env.example`

## Instructor Tips

- Record the live build; pause to explain each "swappable" decision.
- Emphasize the mock-first pattern — it's what separates FDEs from app devs.
