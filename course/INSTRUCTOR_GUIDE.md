# Instructor Guide — How to Produce & Teach FDE101

This guide helps you (Praveen) turn the FDE101 courseware into recorded videos, slides, and a polished product.

**FDE101 has two parts:**
- **Core Track (Local):** Chapters 1–5 — build and deploy the pilot locally (Docker).
- **Bonus Modules (Cloud):** AWS, Azure, GCP — re-deploy the same pilot into a customer cloud.

The same production workflow applies to both core chapters and bonus modules (every `courseware.md` has the same structure).

---

## Production Workflow (per chapter)

1. **Read the `courseware.md`** — it's your full script.
2. **Build slides** — each "Slide N" block = one slide. Titles + bullets are given; speaker notes are your narration.
   - Recommended tools: Gamma.app (fastest), Google Slides, or Keynote.
   - Keep one idea per slide; use the bullets verbatim or tighten.
3. **Record narration** — read the speaker notes naturally. ~3–5 min per slide → ~90 min/chapter.
4. **Record the demo** — screen-record following the demo walkthrough. Run `lab/scripts/demo.sh` first to avoid live failures.
5. **Edit** — captions, zoom on code, trim dead air.
6. **Export resources** — link the `lab/`, `templates/`, and `docs/` files as downloads.

---

## Recommended Recording Setup

| Item | Suggestion |
|------|------------|
| Screen recording | OBS Studio (free) or ScreenFlow |
| Slides | Gamma / Keynote |
| Mic | Any USB condenser; record in a quiet, soft room |
| Editing | DaVinci Resolve (free) or Descript (edit by transcript) |
| Webcam | Optional picture-in-picture for intros/outros |

---

## Chapter Timing & Effort

### Core Track (Local)

| Chapter | Video | Slides | Demo prep | Notes |
|---------|-------|--------|-----------|-------|
| 1 Role & Mindset | ~75 min | 18 | Low | Motivation hook — keep energetic |
| 2 Discovery & Scoping | ~90 min | 18 | Medium (role-play) | Record a full mock call |
| 3 Rapid Prototyping | ~90 min | 18 | Medium (live build) | Use the lab code |
| 4 AI/LLM Integration | ~100 min | 20 | High (flagship) | Most polish here |
| 5 Deploy/Demo/Handoff | ~90 min | 18 | Medium | Capstone walkthrough (local Docker) |

Core total: ~7–8 hours of content + the lab project.

### Bonus Modules (Cloud)

| Module | Video | Slides | Demo prep | Notes |
|--------|-------|--------|-----------|-------|
| A — AWS | ~90 min | 18 | High (needs AWS acct + Bedrock access) | Your strongest module; lead here |
| B — Azure | ~90 min | 18 | High (needs Azure OpenAI approval) | Best for MS-enterprise buyers |
| C — GCP | ~90 min | 18 | High (needs Vertex AI enabled) | Cloud Run = simplest live demo |

Bonus total: ~4–5 hours. Record at least AWS first (highest demand + your expertise).

**Teaching without live cloud:** Each bonus module includes reference IaC (Terraform/Bicep) and CLI steps. If you can't demo live, walk the IaC + console screenshots and run the local pilot beside it to prove identical behavior. The pilot's mock mode means the *flow* is always demoable.

---

## Teaching Principles

- **Show, then explain.** Demo first, theory second, when possible.
- **Always-working demos.** Mock mode (`MOCK_LLM=true`) means no live API failures.
- **One artifact per chapter.** Students should finish each chapter with something tangible.
- **Tie everything to the engagement lifecycle.** Repeat the 5 phases as the spine.

---

## Assessment

- Quiz at the end of each chapter (questions provided in each `courseware.md`).
- Hands-on exercise per chapter (graded in cohort; self-checked in self-paced).
- Final capstone: the deployed pilot + recorded demo + runbook + handoff (Chapter 5).

---

## Course Assets Checklist (before launch)

**Core Track (Local) — required for v1 launch:**
- [ ] 5 chapters recorded + edited
- [ ] Slide decks exported (PDF + source)
- [ ] `lab/` repo cleaned, README verified, runs end-to-end
- [ ] Quizzes built in platform
- [ ] Exercise solutions written
- [ ] Capstone rubric published
- [ ] Welcome + outro videos
- [ ] Certificate of completion template

**Bonus Modules (Cloud) — Pro tier / fast-follow:**
- [ ] AWS module recorded (+ reference Terraform tested)
- [ ] Azure module recorded (+ reference Bicep tested)
- [ ] GCP module recorded (+ reference Terraform tested)
- [ ] Cloud service-mapping cheat sheet exported (`bonus-modules/README.md`)

---

## Recommended Release Strategy

1. **Launch v1 with the Core Track (Local)** — it's complete, zero-cost for students, and proves the full FDE workflow.
2. **Add the cloud bonus modules as a Pro-tier upsell** — record AWS first (highest demand + your expertise), then Azure, then GCP.
3. Students take the **one cloud module** matching their target customer; completionists do all three.

---

## Other Upsell Ideas

- **Interview Prep** — from `docs/interview-prep.md` (mock interviews, comp negotiation)
- **Vector DB Masterclass** — expand `docs/vector-dbs-and-rag-architectures.md`
- **Live cohort** — weekly calls, feedback, community
- **FDE201 (future)** — multi-cloud, security deep-dive, scaling pilots to production
