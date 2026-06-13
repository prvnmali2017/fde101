# Chapter 5 — Deploy, Demo & Handoff

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (deploy + present) + 1 capstone exercise + quiz

---

## Chapter Overview

The pilot works on your laptop — now make it real. Students containerize the app, deploy it, plan the customer-VPC production path, deliver a stakeholder demo that closes the deal, and hand off cleanly. This chapter turns a working prototype into a won engagement and a portfolio piece.

## Learning Objectives

By the end, students can:

1. Containerize and deploy the pilot with Docker
2. Plan a production deployment in a customer AWS environment
3. Write a deployment runbook and complete a handoff checklist
4. Deliver a 10-minute stakeholder demo that drives a decision
5. Propose next steps (expand vs handoff) and close the engagement

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- Chapter 5: Deploy, Demo & Handoff
- "Make it real, then make it theirs"

**Speaker notes:** Final phase of the lifecycle. A pilot that only runs on your machine isn't a deliverable. We deploy, demo, and hand off.

---

### Slide 2 — Why deployment is an FDE skill
- "Works on my machine" ≠ delivered
- Customer environments are messy/locked down
- Your infra background is a moat here

**Speaker notes:** Many AI engineers can build a notebook demo. Few can deploy in a customer's restricted environment. This is where SRE/infra people dominate.

---

### Slide 3 — Containerize with Docker
- One image runs anywhere
- Pin dependencies, bake in data ingest
- `docker compose up` = reproducible

**Speaker notes:** Show `../lab/Dockerfile` and `../lab/docker-compose.yml`. Note the build runs ingestion so the image ships ready-to-serve. Healthcheck included.

---

### Slide 4 — The Dockerfile walkthrough
- Slim base image
- Install deps, copy code
- Run ingestion at build
- Expose port, run uvicorn

**Speaker notes:** Walk each line of the Dockerfile. Explain why we ingest at build (fast cold start) vs runtime (fresh data) — a real trade-off to discuss with customers.

---

### Slide 5 — docker-compose for local prod-like
- Service + env file + volume + healthcheck
- Mirrors how it'll run in prod
- Easy for customer IT to grok

**Speaker notes:** Compose is approachable for customer teams. The healthcheck ties back to the `/health` endpoint from Ch 3.

---

### Slide 6 — Deployment environments
- Pilot: local / single container
- Staging: customer sandbox
- Production: customer VPC

**Speaker notes:** Progression. Each step adds constraints (security, scale, monitoring). Don't skip straight to prod.

---

### Slide 7 — Production in a customer AWS account
- Compute: ECS Fargate / EKS
- Vector store: OpenSearch Serverless
- LLM: Bedrock (data stays in VPC)
- Secrets: Secrets Manager

**Speaker notes:** Show `../lab/deliverables/deployment-runbook.md` "Production Migration" section. This is the swap path we designed for in Ch 3–4. Tie to student's/your infra skills.

---

### Slide 8 — Enterprise deployment concerns
- Network: private subnets, VPC peering
- Identity: IAM roles, SSO
- Data: residency, retention, PII
- Compliance: audit logs

**Speaker notes:** These are the questions that kill or close enterprise deals. Surface them in discovery (Ch 2), solve them here. Your IAM/security background is the asset.

---

### Slide 9 — The deployment runbook
- Step-by-step deploy instructions
- Config/secrets inventory (references, not values)
- Rollback procedure
- Support contacts

**Speaker notes:** Walk `../lab/deliverables/deployment-runbook.md`. A runbook is what lets the customer operate it after you leave. It's a deliverable, not an afterthought.

---

### Slide 10 — Observability (your edge)
- `/health` + metrics
- Latency, error rate, retrieval quality
- Alerts with runbook links

**Speaker notes:** SRE habits = customer trust. Even a pilot benefits from basic metrics. Mention CloudWatch/Prometheus + OpenTelemetry as the production add-on.

---

### Slide 11 — Now: the demo that closes
- Code working ≠ deal won
- The demo converts work into decision
- Audience = decision-makers, not engineers

**Speaker notes:** Shift from building to selling the build. The demo is the highest-leverage 10 minutes of the engagement.

---

### Slide 12 — Demo structure (10 min)
1. Set the scene (1 min)
2. Show the interface (30s)
3. Live flow: 3 questions + 1 action (5 min)
4. Results + metrics (2 min)
5. Next steps (1.5 min)

**Speaker notes:** Walk `../lab/deliverables/demo-script.md`. A scripted demo beats improvisation. Rehearse it.

---

### Slide 13 — Demo do's and don'ts
- DO lead with business outcome
- DO show, don't tell
- DON'T show code to executives
- DON'T wing it — run the smoke test first

**Speaker notes:** Run `scripts/demo.sh` before going live. The #1 demo failure is an unrehearsed live mistake. Have a recorded backup.

---

### Slide 14 — Handling tough questions
- "What if it's wrong?" → cites sources, agents verify, we log
- "Is our data safe?" → mock/Bedrock, in-VPC
- "How long to prod?" → 3–4 weeks post security sign-off

**Speaker notes:** Show the Q&A table in the demo script. Prepared answers to predictable objections build executive confidence.

---

### Slide 15 — Proving value with metrics
- Before/after where possible
- Eval score (RetailCo: 14/15)
- Latency, tickets deflected (projected)

**Speaker notes:** Numbers turn "neat demo" into "fund this." Tie back to the success metric agreed in discovery (Ch 2). Close the loop.

---

### Slide 16 — The handoff
- Knowledge transfer session
- Repos/access transferred
- Runbook + "how to add docs" guide
- On-call for first 2 weeks

**Speaker notes:** Walk `../templates/handoff-checklist.md`. A clean handoff = renewals and referrals. Sloppy handoff = support burden and churn.

---

### Slide 17 — Expand vs handoff
- Expand: more use cases, production build
- Handoff: customer team takes over
- Always propose a concrete next phase

**Speaker notes:** Land & expand is the FDE business model. Even a handoff should include a next-phase proposal. Never end with silence.

---

### Slide 18 — Course capstone recap
- You ran discovery → scoped → built RAG+agent → deployed → demoed → handed off
- You have a portfolio project + interview stories
- You ARE an FDE now

**Speaker notes:** Celebrate. They completed a full engagement. Point them to `../docs/interview-prep.md` to land the role. Ask for a testimonial (helps you sell!).

---

## Demo (Instructor-led): Deploy + Present

**Goal:** Containerize, run prod-like, and deliver the closing demo.

**Walkthrough script:**

1. Show `../lab/Dockerfile` and `docker-compose.yml`.
2. Deploy:
   ```bash
   cd ../lab
   docker compose up --build -d
   docker compose logs -f api
   curl http://localhost:8000/health
   ```
3. Walk the deployment runbook (`deliverables/deployment-runbook.md`), including the AWS production section.
4. Switch hats to "demo day": follow `deliverables/demo-script.md` end-to-end against the running container.
5. Show the handoff checklist (`../templates/handoff-checklist.md`) as the closing deliverable.

**Takeaway:** From laptop to deployed, demoed, and handed-off — a complete engagement.

---

## Capstone Exercise

**Title:** Deliver your engagement end-to-end

**Instructions for students:**
1. `docker compose up --build` your pilot and confirm `/health`.
2. Complete the deployment runbook for your version (including a production sketch).
3. Record a 5–10 minute demo following the demo-script structure.
4. Complete the handoff checklist.
5. Write a one-paragraph "next phase" proposal (expand or handoff).

**Deliverable:** Running container + recorded demo + completed runbook + handoff checklist + next-phase proposal. **This is the portfolio capstone.**

**Solution notes (instructor):** Grade on: does it deploy cleanly, does the demo lead with outcomes, is the runbook usable by someone else, is there a concrete next step. This artifact is what students show in interviews.

---

## Quiz (5 questions)

1. Why is deployment a competitive edge for ex-SRE/infra FDEs? *(customer environments are restricted; few AI engineers can deploy there)*
2. What belongs in a deployment runbook? *(steps, config/secrets inventory, rollback, contacts)*
3. Who is the audience for the closing demo, and what do you lead with? *(decision-makers; lead with business outcome)*
4. Name two enterprise deployment concerns to raise in discovery. *(data residency/PII, IAM/SSO, network, compliance)*
5. What's the difference between "expand" and "handoff," and why always propose a next phase? *(more scope vs customer takes over; momentum drives renewals/referrals)*

---

## Downloadable Resources

- Dockerfile + compose → `../lab/Dockerfile`, `../lab/docker-compose.yml`
- Deployment runbook → `../lab/deliverables/deployment-runbook.md`
- Demo script → `../lab/deliverables/demo-script.md`
- Handoff checklist → `../templates/handoff-checklist.md`
- Interview prep (bonus) → `../docs/interview-prep.md`

## Instructor Tips

- The capstone is the selling point — make students proud to show it.
- Collect demo recordings (with permission) as testimonials/social proof.
- End the course with a clear "what next": apply, with the portfolio project in hand.
