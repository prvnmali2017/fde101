# FDE101 — Forward Deployed Engineer Bootcamp & Learning Kit

A complete program to become a **Forward Deployed Engineer (FDE)**: course, hands-on lab, reference docs, and customer-delivery templates.

Built by **Praveen Mali** — 14+ years in platform/SRE + AI Ops.

## Repository Layout

```
fde101/
├── README.md                  ← You are here
├── course/                    ← FDE101 courseware (sellable online course)
│   ├── README.md              ← Course overview, curriculum, pricing
│   ├── INSTRUCTOR_GUIDE.md
│   ├── DEMOS.md               ← All demos compiled in one place
│   ├── selling/go-to-market.md
│   ├── chapter-01..05/        ← Core (Local) track
│   ├── bonus-modules/         ← AWS, Azure, GCP cloud modules
│   └── slides/                ← mlopsguru-branded slide pipeline (Marp)
├── lab/                       ← RetailCo AI Support Pilot (runnable)
├── docs/                      ← Skills map, learning path, RAG/vector deep-dive, interview prep
└── templates/                 ← Discovery, pilot plan, handoff checklist
```

## Quick Start

**Run the lab:**
```bash
cd lab
cp .env.example .env
./scripts/setup.sh
source .venv/bin/activate
uvicorn src.api.main:app --reload --port 8000
```
Open http://localhost:8000.

**Build slides:**
```bash
cd course/slides
./build.sh
```

## Recommended Order

1. `docs/skills-map.md` — identify your gaps
2. `docs/learning-path.md` — 4-week plan
3. `lab/` — build and demo the pilot
4. `templates/` — practice customer-facing artifacts
5. `docs/interview-prep.md` — frame your stories
6. `course/` — package and sell it

## The Lab Scenario

**RetailCo** wants an AI assistant that answers support questions from internal docs and looks up order status. You have 2 weeks to deliver a working pilot — exactly the kind of engagement an FDE owns.
