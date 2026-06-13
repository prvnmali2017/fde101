# Chapter 2 — Customer Discovery & Scoping

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (discovery role-play) + 1 exercise + quiz

---

## Chapter Overview

The #1 reason pilots fail is solving the wrong problem. This chapter teaches the FDE's most underrated skill: talking to customers to uncover real pain, then scoping a bounded pilot that can actually ship in 2 weeks. Students produce a real pilot plan for RetailCo.

## Learning Objectives

By the end, students can:

1. Run a structured discovery call using a repeatable framework
2. Distinguish real pain from feature requests ("The Mom Test")
3. Define measurable success criteria with a customer
4. Scope a 2–4 week pilot and ruthlessly cut non-essentials
5. Produce a one-page pilot plan

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- Chapter 2: Customer Discovery & Scoping
- "Solve the right problem, then make it small"

**Speaker notes:** Remind students of the lifecycle — we're in phases 1 & 2 (Discover, Scope). This is where engagements are won or lost before a line of code.

---

### Slide 2 — Why discovery matters
- 60%+ of projects fail on wrong-problem, not bad code
- Customers ask for solutions, not problems
- Your job: dig to the real pain

**Speaker notes:** Tell a story (yours or a generic one) of a project that built the wrong thing. The lesson: requirements as given are almost always wrong or incomplete.

---

### Slide 3 — The buyer vs the user
- Buyer: signs the check, wants ROI
- User: does the work, wants relief
- Talk to BOTH — they want different things

**Speaker notes:** RetailCo example: Sarah (Director, buyer) wants ticket deflection; the 15 agents (users) want faster answers. Solve for both or adoption fails.

---

### Slide 4 — The Mom Test (core principle)
- Don't ask "Would you use this?" (people lie to be nice)
- Ask about their **past behavior and real problems**
- Good: "Walk me through the last time this happened"

**Speaker notes:** Introduce Rob Fitzpatrick's "The Mom Test." The trick: ask questions even your mom couldn't lie about. Facts about the past, not opinions about the future.

---

### Slide 5 — Bad vs good discovery questions
| Bad (leading) | Good (factual) |
|---------------|----------------|
| "Would an AI bot help?" | "How do you handle repeat questions today?" |
| "Is this a big problem?" | "How many hours/week does this take?" |
| "Would you pay for this?" | "What have you tried, and what did it cost?" |

**Speaker notes:** Walk each pair. The good questions extract numbers and real history you can scope against.

---

### Slide 6 — The discovery framework (6 parts)
1. Context
2. Current pain
3. Success criteria
4. Technical landscape
5. Scope boundaries
6. Next steps

**Speaker notes:** This maps directly to `../templates/discovery-call-template.md`. Tell students to keep it open during real calls.

---

### Slide 7 — Part 1: Context
- What does the company do?
- Why now? What triggered this?
- Who owns the outcome?

**Speaker notes:** "Why now" surfaces urgency and budget. No urgency = no pilot.

---

### Slide 8 — Part 2: Current pain
- What's broken/slow today?
- How many people affected?
- What have they tried?
- Quantify: time, money, tickets

**Speaker notes:** Numbers here become your success metrics later. Always leave with quantities.

---

### Slide 9 — Part 3: Success criteria
- "What does success look like in 2 weeks?"
- Pick ONE primary metric
- Who approves moving past pilot?

**Speaker notes:** Force a single primary metric. RetailCo: 80% correct on a 15-question eval set. Measurable = demoable.

---

### Slide 10 — Part 4: Technical landscape
- Cloud / on-prem?
- Identity (SSO)?
- Where's the data? APIs available?
- Security/compliance constraints?

**Speaker notes:** This is where your infra background shines. Surface blockers EARLY — security review can kill timelines.

---

### Slide 11 — Part 5: Scope boundaries
- In scope / out of scope (write both)
- Assumptions
- Risks

**Speaker notes:** Writing "out of scope" explicitly is a superpower — it manages expectations and prevents scope creep.

---

### Slide 12 — Part 6: Next steps
- Validate notes with customer
- Draft pilot plan
- Identify technical point of contact

**Speaker notes:** Always end a call with a concrete next step and an owner. Momentum is trust.

---

### Slide 13 — From discovery to scope
- Discovery gives you a problem + constraints
- Scoping turns it into a buildable slice
- The art: cut until it fits 2 weeks

**Speaker notes:** Transition from listening to deciding. The next slides are about ruthless cutting.

---

### Slide 14 — The scoping principle: thin vertical slice
- Build one complete path end-to-end
- NOT every feature half-done
- One question answered well > ten features broken

**Speaker notes:** Draw it: a thin vertical slice through all layers beats a wide-but-shallow build. RetailCo slice: "answer a return-policy question with a citation."

---

### Slide 15 — Scoping techniques
- MoSCoW: Must / Should / Could / Won't
- Mock the hard integrations first
- Defer anything needing long approvals
- Timebox each phase

**Speaker notes:** "Won't (this pilot)" is the most powerful column. Mocking lets you start before access is granted — the lab mocks the order API.

---

### Slide 16 — RetailCo scope worked example
- IN: 3 policy docs, order lookup, 15 agents, local deploy
- OUT: customer-facing bot, full Confluence migration, prod VPC
- Assumption: sandbox order API available
- Risk: security review of LLM data flow

**Speaker notes:** Show `../lab/deliverables/discovery-notes.md`. This is a real scoped pilot they'll build in Ch 3–5.

---

### Slide 17 — The pilot plan document
- Executive summary
- Objectives + metrics
- Timeline (weekly milestones)
- Risks + mitigations
- Exit criteria

**Speaker notes:** Walk `../templates/pilot-plan-template.md`. This one-pager is what you send the customer to align before building.

---

### Slide 18 — Common scoping mistakes
- Boiling the ocean (too big)
- Vague success ("make it better")
- Ignoring security timelines
- No single decision-maker

**Speaker notes:** Each of these has killed real pilots. Closing message: a small shipped pilot beats a big planned one every time.

---

## Demo (Instructor-led): Discovery Role-Play

**Goal:** Model a real discovery call and turn it into notes.

**Walkthrough script:**

1. Play both roles (or invite a guest): you = FDE, "Sarah Chen" = RetailCo Support Director.
2. Run through the 6-part framework live, asking Mom Test-style questions:
   - "Walk me through what your agents do when a return question comes in."
   - "How many of those 400 daily tickets are repeats?"
   - "If this worked, what number would change?"
3. Take live notes on screen using `../templates/discovery-call-template.md`.
4. Convert notes into the scoped pilot in `../lab/deliverables/discovery-notes.md`.
5. Highlight the in/out-of-scope decisions and the single success metric.

**Takeaway:** Discovery is a learnable script, not charisma.

---

## Hands-On Exercise

**Title:** Run discovery and scope a pilot

**Instructions for students:**
1. Pair up (cohort) or use the provided RetailCo transcript (self-paced).
2. Fill out the full discovery template.
3. Produce a one-page pilot plan with: one primary metric, in/out scope, 2-week timeline, top risk.

**Deliverable:** Completed `discovery-call-template.md` + `pilot-plan-template.md`.

**Solution notes (instructor):** Reward a single measurable metric and an explicit "out of scope" list. Flag plans where the build can't finish in 2 weeks.

---

## Quiz (5 questions)

1. What is the core idea of "The Mom Test"? *(ask about past behavior/facts, not future opinions)*
2. Why talk to both the buyer and the user? *(they want different outcomes; both needed for ROI + adoption)*
3. What is a "thin vertical slice"? *(one complete end-to-end path vs many half-features)*
4. Which MoSCoW column most protects your timeline? *(Won't)*
5. Name one risk that commonly blows up pilot timelines. *(security/compliance review, data access approvals)*

---

## Downloadable Resources

- Discovery template → `../templates/discovery-call-template.md`
- Pilot plan template → `../templates/pilot-plan-template.md`
- Worked example → `../lab/deliverables/discovery-notes.md`
- Customer brief → `../lab/customer-brief.md`

## Instructor Tips

- Role-play sells this chapter — record at least one full mock call.
- Push students hard on cutting scope; most cut too little.
