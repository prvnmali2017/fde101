# Demo Script — RetailCo Support AI Pilot

**Audience:** Sarah Chen (Support Director) + 2 team leads
**Duration:** 10 minutes
**Format:** Live demo + Q&A

---

## 1. Set the Scene (1 min)

> "Sarah, over the last two weeks we built an internal assistant for your support team. It answers policy questions from your official docs — with citations — and looks up order status in real time. Let me show you."

## 2. Show the Interface (30 sec)

Open http://localhost:8000

> "This is what your agents would see. Simple chat — no training needed. Behind the scenes it searches your shipping, returns, and warranty policies, and connects to your order system."

## 3. Demo Flow (5 min)

### Question 1 — Policy (Return)
Type: **"What is the return policy?"**

> "Notice it cites the Returns & Refunds Policy and gives the 30-day window, restocking fee rules, and refund timeline. The agent doesn't have to search Confluence."

### Question 2 — Policy (Shipping)
Type: **"How long does standard shipping take?"**

> "5–7 business days metro, 7–10 regional — pulled directly from your shipping policy doc."

### Question 3 — Order Lookup
Type: **"What's the status of order ORD-1001?"**

> "Here it called your order API automatically. Status: Delivered, with tracking number. This is what the previous chatbot couldn't do."

### Question 4 — Edge Case
Type: **"Can I return an opened pillow?"**

> "It knows opened personal care items have special rules. If it's unsure, it says so instead of guessing."

## 4. Show the API (1 min, optional for technical audience)

Open http://localhost:8000/docs

> "Your IT team gets full API docs. This can integrate into Zendesk as a sidebar plugin in Phase 2."

## 5. Results & Next Steps (2 min)

> "We tested against 15 common questions — 14/15 correct. Order lookups average under 1 second locally.
>
> **Recommended next steps:**
> 1. 3-day trial with your 15 pilot agents
> 2. Security review for production LLM (Bedrock — keeps data in your AWS account)
> 3. Migrate vector store to OpenSearch for production
>
> I've left a deployment runbook and handoff checklist with James's team."

## 6. Handle Common Questions

| Question | Answer |
|----------|--------|
| "What if it gives wrong answers?" | It cites sources — agents verify. We log all queries for review. |
| "Is customer data sent to OpenAI?" | Pilot uses mock mode. Production plan: Bedrock in your VPC, no external data transfer. |
| "How long to production?" | 3–4 weeks after security sign-off. |
| "Can it deflect customer tickets directly?" | Phase 2 — customer-facing widget. This pilot is agent-assist first. |

---

## Demo Checklist

- [ ] Server running (`uvicorn` or Docker)
- [ ] Browser open to http://localhost:8000
- [ ] Test all 4 questions beforehand
- [ ] Deployment runbook printed or shared
- [ ] Eval results ready (14/15 or run `./scripts/demo.sh`)
