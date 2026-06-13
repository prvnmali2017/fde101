# Chapter 1 — The Forward Deployed Engineer Role & Mindset

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (engagement mapping) + 1 exercise + quiz

---

## Chapter Overview

This chapter sells the dream and sets the foundation. Students learn what an FDE actually does, why it's one of the highest-leverage roles in tech, the engagement lifecycle they'll master, and the mindset shift from "internal engineer" to "customer-facing builder."

## Learning Objectives

By the end of this chapter, students can:

1. Define the FDE role and distinguish it from SWE, SRE, SA, and consultant roles
2. Describe the 5-phase FDE engagement lifecycle
3. Identify which companies hire FDEs and what they pay
4. Apply the three core FDE mindset principles to a scenario
5. Map a real-world problem to an FDE engagement

---

## Slide Deck (slide-by-slide)

> Build these in your slide tool. Each block = one slide. **Speaker notes** are your recording script.

### Slide 1 — Title
- **The Forward Deployed Engineer Bootcamp**
- Chapter 1: The Role & Mindset
- Your name + tagline: "From backend engineer to customer-facing builder"

**Speaker notes:** Welcome students. State the promise: by the end of this course they'll have built and deployed a real AI pilot and be able to interview for FDE roles paying $180k–$350k+. This chapter is the "why" and "what."

---

### Slide 2 — What you'll learn this chapter
- What an FDE actually does (day in the life)
- The engagement lifecycle
- Who hires FDEs & comp
- The 3 mindset shifts
- Your course project preview

**Speaker notes:** Set expectations. Tell them this chapter is lighter on code, heavy on framing — but framing is what makes the difference between a coder and a deployed engineer.

---

### Slide 3 — What is a Forward Deployed Engineer?
- An engineer who **embeds with customers** to build and deploy solutions
- Lives at the intersection of: **product + engineering + customer success**
- Coined/popularized by Palantir; now everywhere in AI (OpenAI, Anthropic, Scale, Cursor, Databricks)

**Speaker notes:** The FDE goes *to the customer* (physically or virtually), understands their problem deeply, and builds a working solution — often a thin slice of the product glued to messy customer data. They are trusted technical people who can both code and talk to executives.

---

### Slide 4 — The one-sentence definition
- > "An FDE turns a customer's vague problem into a working, deployed solution — fast."
- Three keywords: **vague → working → fast**

**Speaker notes:** Repeat this. Everything in the course ladders up to these three words. Vague (discovery), working (build), fast (scope + deploy).

---

### Slide 5 — A day in the life
- Morning: customer standup, understand a blocker
- Midday: build/integrate — code against their API
- Afternoon: demo progress to stakeholder
- Always: write things down (runbooks, decisions)

**Speaker notes:** Contrast with a normal SWE day (tickets, PRs, internal). The FDE context-switches between code and customer constantly. Emphasize communication is half the job.

---

### Slide 6 — FDE vs other roles
| Role | Focus | Customer contact |
|------|-------|------------------|
| SWE | Build product features | Rare |
| SRE | Keep systems reliable | Internal |
| Solutions Architect | Design, advise | High, but less hands-on coding |
| Consultant | Advise, strategy | High, little code |
| **FDE** | **Build + deploy at customer** | **High + hands-on code** |

**Speaker notes:** The FDE is the rare combination: deep hands-on building AND high customer contact. That combination is why it's scarce and well-paid.

---

### Slide 7 — Why FDE is high-leverage
- You directly drive revenue (land & expand)
- You see the product AND the market
- Fast path to product, founding eng, or leadership
- AI made FDEs critical: products are powerful but need customer-specific glue

**Speaker notes:** Explain that AI products are general; customers need them wired into their specific data and workflows. That glue work is the FDE's bread and butter — and it's exploding in demand.

---

### Slide 8 — Who hires FDEs
- Palantir (the original)
- AI labs: OpenAI, Anthropic
- AI infra/tools: Scale AI, Databricks, Cursor, Cohere
- Defense/hard-tech: Anduril
- Many startups (often titled "Solutions Engineer" or "Deployment Engineer")

**Speaker notes:** Tell students to search "forward deployed", "deployment engineer", "solutions engineer", "field engineer". Same role, different titles.

---

### Slide 9 — Compensation
- US: ~$180k–$350k+ total comp (senior)
- Strong equity component at startups
- Premium for: AI/LLM skills + infra + customer skills
- Your edge: most engineers lack the customer half

**Speaker notes:** Be honest that numbers vary by region and seniority. The point: it pays well because the skill combination is rare. This course builds the rare half.

---

### Slide 10 — The FDE Engagement Lifecycle (the course spine)
1. **Discover** — find the real problem (Ch 2)
2. **Scope** — define a bounded pilot (Ch 2)
3. **Build** — ship a working prototype (Ch 3 & 4)
4. **Deploy** — get it running in their world (Ch 5)
5. **Handoff / Expand** — close the loop (Ch 5)

**Speaker notes:** This is the map for the whole course. Each chapter is a phase. Show students where they are. Everything they build maps to a real engagement phase.

---

### Slide 11 — Phase 1: Discover
- Talk to users, not just buyers
- Find the pain behind the ask
- Output: validated problem statement

**Speaker notes:** Most failed projects solve the wrong problem. Tease Chapter 2's discovery framework and "The Mom Test."

---

### Slide 12 — Phase 2: Scope
- Time-box: 2–4 week pilots
- Cut ruthlessly to a demonstrable slice
- Output: pilot plan with success criteria

**Speaker notes:** Scope is where FDEs win or lose. A pilot that's too big never ships. Tease the pilot plan template.

---

### Slide 13 — Phase 3: Build
- Ship the thinnest working thing
- Mock what you can't access yet
- Output: working prototype

**Speaker notes:** Introduce the "mock first" principle — you'll often start with fake data and swap in real integrations later. The course lab does exactly this.

---

### Slide 14 — Phase 4: Deploy
- Run it in a customer-like environment
- Security, access, data residency matter
- Output: deployed pilot + runbook

**Speaker notes:** This is where infra/SRE background shines. Deploying in someone else's environment is a skill — Docker, IAM, networks, secrets.

---

### Slide 15 — Phase 5: Handoff / Expand
- Demo to decision-makers
- Hand off cleanly OR expand scope
- Output: signed-off pilot, next-phase proposal

**Speaker notes:** The engagement isn't done when the code works — it's done when the customer can run it or decides to buy more. Tease the handoff checklist.

---

### Slide 16 — Mindset Shift #1: Outcomes over output
- Customers don't care about your clean code
- They care about their problem being solved
- Measure success in *their* metrics (tickets deflected, hours saved)

**Speaker notes:** Hard pill for engineers. A hacky solution that solves the problem beats elegant code that doesn't ship. Reframe pride around customer outcomes.

---

### Slide 17 — Mindset Shift #2: Communication is the job
- Demos > documents
- Write decisions down
- Translate tech ↔ business constantly
- Silence kills trust — over-communicate progress

**Speaker notes:** Give the rule: a working demo every few days beats a perfect system in a month. Customers fund momentum.

---

### Slide 18 — Mindset Shift #3: Bias to action under ambiguity
- You'll never have full requirements
- Make a reasonable assumption, build, validate
- Speed of learning > speed of coding

**Speaker notes:** FDEs operate in fog. The skill is making progress anyway and correcting fast. Close the chapter by connecting all three mindsets to the project they'll build.

---

## Demo (Instructor-led): Mapping an Engagement

**Goal:** Show students how a vague customer ask becomes a 5-phase engagement.

**Walkthrough script:**

1. Open `../lab/customer-brief.md` on screen.
2. Read RetailCo's vague ask aloud: *"We want an AI assistant for support."*
3. Live-annotate it against the 5 phases:
   - Discover → "What's the real pain? 400 tickets/day, repeat questions"
   - Scope → "2-week pilot: FAQ answers + order lookup, 15 agents"
   - Build → "FastAPI + RAG + order tool" (preview the lab)
   - Deploy → "Docker locally, AWS for production"
   - Handoff → "Demo to Sarah Chen, runbook for IT"
4. Show the finished lab running (`uvicorn` + browser at localhost:8000) as a "here's where we're going" teaser.

**Takeaway for students:** Every engagement, no matter how vague, fits this map.

---

## Hands-On Exercise

**Title:** Map your own engagement

**Instructions for students:**
1. Pick a problem from your current job OR use this prompt: *"A logistics company wants to reduce time spent answering 'where is my shipment' emails."*
2. Write one paragraph per phase (Discover, Scope, Build, Deploy, Handoff).
3. For Scope, force yourself to a 2-week pilot — what's the smallest demonstrable slice?

**Deliverable:** A 1-page engagement map (template provided in `../templates/pilot-plan-template.md`).

**Solution notes (for instructor):** Strong answers narrow scope aggressively. A common mistake is a "boil the ocean" build phase. Praise students who mock data and defer integrations.

---

## Quiz (5 questions)

1. In one sentence, what does an FDE do? *(vague → working → fast)*
2. Name two ways an FDE differs from a Solutions Architect. *(hands-on coding; builds + deploys)*
3. List the 5 phases of the engagement lifecycle. *(Discover, Scope, Build, Deploy, Handoff/Expand)*
4. Why did AI increase demand for FDEs? *(general products need customer-specific integration glue)*
5. Which mindset shift addresses "you'll never have full requirements"? *(Bias to action under ambiguity)*

---

## Downloadable Resources for This Chapter

- Engagement map template → `../templates/pilot-plan-template.md`
- Customer scenario → `../lab/customer-brief.md`
- Bonus reading list → `../courses/README.md`

## Instructor Tips

- Keep this chapter energetic — it's the motivation hook that reduces refunds.
- End with the finished-lab teaser so students are excited to build.
- Encourage students to post their engagement map in the community/cohort channel.
