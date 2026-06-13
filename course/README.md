# FDE101 — The Forward Deployed Engineer Bootcamp

**A practical, sellable online course that teaches engineers how to become Forward Deployed Engineers (FDEs).**

Built by Praveen Mali — 14+ years in platform/SRE + AI Ops — FDE101 turns experienced backend/infra/SRE engineers into customer-facing FDEs who can discover problems, build AI-powered pilots, and deploy them in customer environments.

> **Course code:** FDE101 (foundation level). Future levels (FDE201/301) can go deeper on multi-cloud, security, and scale.

---

## Who This Course Is For

| Audience | Why they buy |
|----------|--------------|
| Backend / SRE / DevOps engineers | Pivot into higher-paid, customer-facing FDE roles |
| Full-stack devs eyeing AI roles | Learn enterprise AI delivery (RAG, agents) |
| Solutions engineers / SAs | Add hands-on building to their consulting skills |
| Bootcamp grads with fundamentals | Differentiate with a real, deployable portfolio project |

**Prerequisite:** Comfortable with one programming language (Python preferred), basic Git, basic cloud concepts.

---

## What Students Build

By the end, every student has shipped the **RetailCo AI Support Pilot** — a working RAG + agent application with a real deployment runbook and demo. This is their portfolio centerpiece and interview proof.

The pilot is built **locally first** (zero cloud cost), then students choose a **cloud bonus module** (AWS, Azure, or GCP) to deploy it into a real customer-style environment.

---

## Course Map

FDE101 has two parts: the **Core (Local) Track** and the **Bonus Cloud Modules**.

```
FDE101
│
├── CORE TRACK (Local) ──────────────────────────────────────────
│   Ch 1  The FDE Role & Mindset
│   Ch 2  Customer Discovery & Scoping
│   Ch 3  Rapid Prototyping & Integration
│   Ch 4  AI/LLM Integration: RAG & Agents
│   Ch 5  Deploy, Demo & Handoff   ← deploys LOCALLY (Docker)
│
└── BONUS MODULES (Cloud) ──────────────────────────────────────
    Bonus A  Deploy for AWS Customers
    Bonus B  Deploy for Azure Customers
    Bonus C  Deploy for GCP Customers
    (Take the one that matches your target customer / employer)
```

### Core Track (Local) — Chapters 1–5

| # | Chapter | Outcome | Demo (runs locally) |
|---|---------|---------|---------------------|
| 1 | **The FDE Role & Mindset** | Understand the job and engagement lifecycle | Map a real engagement |
| 2 | **Customer Discovery & Scoping** | Run discovery, scope a 2-week pilot | Discovery role-play + pilot plan |
| 3 | **Rapid Prototyping & Integration** | FastAPI backend + customer integration | Working API + order lookup tool |
| 4 | **AI/LLM Integration: RAG & Agents** | Add retrieval + agentic tool use | RAG over docs + agent demo |
| 5 | **Deploy, Demo & Handoff** | Deploy with Docker, present, hand off | Docker deploy + live demo |

### Bonus Modules (Cloud)

Each bonus module takes the **same RetailCo pilot** and re-deploys it using that cloud's **managed, FDE-relevant services** — so students can deliver in a real customer account.

| Module | For customers on... | Maps to |
|--------|---------------------|---------|
| **Bonus A — AWS** | Amazon Web Services | ECS/App Runner, Bedrock, OpenSearch Serverless, ECR, Secrets Manager |
| **Bonus B — Azure** | Microsoft Azure | Container Apps, Azure OpenAI, Azure AI Search, ACR, Key Vault |
| **Bonus C — GCP** | Google Cloud | Cloud Run, Vertex AI (Gemini), Vertex AI Vector Search, Artifact Registry, Secret Manager |

See `bonus-modules/README.md` for the side-by-side service comparison.

Each chapter/module = **~90 min of video** + slides + 1 demo + 1 hands-on exercise + quiz.

---

## Repository Structure

```
course/
├── README.md                    # You are here (FDE101 overview)
├── INSTRUCTOR_GUIDE.md          # How to record/produce each chapter
├── selling/
│   └── go-to-market.md          # Pricing, platforms, launch plan
├── chapter-01-fde-role-mindset/courseware.md      # CORE (Local)
├── chapter-02-discovery-scoping/courseware.md     # CORE (Local)
├── chapter-03-rapid-prototyping/courseware.md     # CORE (Local)
├── chapter-04-ai-llm-integration/courseware.md    # CORE (Local)
├── chapter-05-deploy-demo-handoff/courseware.md   # CORE (Local)
└── bonus-modules/
    ├── README.md                # Cloud comparison + how to choose
    ├── aws/courseware.md        # BONUS A — AWS customers
    ├── azure/courseware.md      # BONUS B — Azure customers
    └── gcp/courseware.md        # BONUS C — GCP customers
```

---

## What's In Each Chapter/Module Folder

Each `courseware.md` contains everything needed to **record videos, build slides, and run demos**:

- Chapter overview + learning objectives
- Slide-by-slide deck (titles + bullets + speaker notes / script)
- Instructor-led demo walkthrough (tied to the working `../lab/`)
- Hands-on exercise + solution notes
- Quiz with answers
- Downloadable resources

---

## How to Use This to Create & Sell

1. **Build slides** — each `courseware.md` has a slide-by-slide outline. Drop into Keynote/Google Slides/Gamma.
2. **Record** — use the speaker notes as your script.
3. **Demo** — follow the demo walkthrough; working code lives in `../lab/`.
4. **Package** — bundle videos + slides + the `lab/` repo as the downloadable project.
5. **Sell** — see `selling/go-to-market.md` for platforms, pricing, and launch plan.

---

## Suggested Pricing & Format

| Tier | Price (USD) | Includes |
|------|-------------|----------|
| Self-paced | $149–$299 | Core track videos, slides, lab repo, quizzes |
| Pro | $399–$599 | + All 3 cloud bonus modules + certificate |
| Cohort | $799–$1,499 | + Live sessions, mock interviews, feedback |
| Corporate | $5k+ /team | Team workshop + custom scenario |

The **cloud bonus modules are a natural upsell** (Pro tier and above).

See `selling/go-to-market.md` for the full launch playbook.

---

## Companion Assets (already in this repo)

- `../lab/` — the RetailCo pilot students build (runs locally, verified working)
- `../docs/vector-dbs-and-rag-architectures.md` — Chapter 4 + bonus modules deep-dive reference
- `../templates/` — discovery, pilot plan, handoff templates
- `../docs/interview-prep.md` — bonus interview module material
