# Chapter 4 — AI/LLM Integration: RAG & Agents

**Duration:** ~90 minutes
**Format:** 20 slides + 1 demo (add the AI brain) + 1 exercise + quiz

---

## Chapter Overview

This is the course's differentiator. Students add the AI brain: a RAG pipeline that answers from customer documents with citations, and an agent that calls tools (order lookup). They learn vector DBs, chunking, prompts, and the pilot→production AI migration path. This is the highest-value, most marketable chapter.

## Learning Objectives

By the end, students can:

1. Explain RAG and when to use it vs fine-tuning
2. Build an ingestion pipeline (chunk → embed → store) with a vector DB
3. Wire retrieval into an LLM prompt with citations
4. Implement agentic tool use (LLM decides to call `lookup_order`)
5. Choose a vector DB and RAG pattern for a given customer
6. Run the pilot in mock mode (no API key) for demos and security reviews

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- Chapter 4: AI/LLM Integration — RAG & Agents
- "Give the pilot a brain"

**Speaker notes:** This is why customers hire AI FDEs. We turn the Ch 3 skeleton into an assistant that answers from their docs and takes actions.

---

### Slide 2 — The problem with raw LLMs
- LLMs don't know your customer's data
- They hallucinate confidently
- They can't take actions on their own

**Speaker notes:** Frame the two fixes: RAG (give it knowledge) and tools/agents (give it actions). The rest of the chapter is these two.

---

### Slide 3 — What is RAG?
- Retrieval-Augmented Generation
- Fetch relevant docs → put in prompt → LLM answers grounded
- Answers cite real sources

**Speaker notes:** Reference `../docs/vector-dbs-and-rag-architectures.md` as the deep-dive companion. RAG = open-book exam for the LLM.

---

### Slide 4 — RAG vs fine-tuning
| | RAG | Fine-tuning |
|--|-----|-------------|
| Update data | Re-index (minutes) | Retrain (expensive) |
| Citations | Yes | No |
| Best for | Changing knowledge | Changing behavior/style |

**Speaker notes:** FDE default is RAG — customer docs change constantly and citations build trust. Fine-tuning is rare in pilots.

---

### Slide 5 — The RAG pipeline
```
Docs → Chunk → Embed → Vector DB
Query → Embed → Search → Prompt+context → LLM → Answer
```

**Speaker notes:** Walk each step. This maps to `../lab/src/ingest/rag.py`. Tell students we'll build ingestion, then retrieval.

---

### Slide 6 — Embeddings explained
- Text → vector of numbers capturing meaning
- Similar meaning = close vectors
- Search = nearest neighbors to the query vector

**Speaker notes:** Keep intuitive. "King - man + woman ≈ queen" style. The model converts text to coordinates; we find nearby coordinates.

---

### Slide 7 — Chunking strategies
- Fixed window (256–512 tokens, overlap)
- Paragraph/section based (the lab)
- Semantic / parent-child (advanced)

**Speaker notes:** Show `_chunk_text()` in the lab. Chunking quality drives answer quality as much as the model. Too big = noisy; too small = lost context.

---

### Slide 8 — Vector database landscape
- ChromaDB (local/dev — the lab)
- pgvector (already-on-Postgres)
- OpenSearch / Bedrock KB (AWS production)
- Pinecone / Weaviate / Qdrant (SaaS/self-host)

**Speaker notes:** Reference the full matrix in `../docs/vector-dbs-and-rag-architectures.md`. For pilots: Chroma or Bedrock KB. For prod: OpenSearch or pgvector.

---

### Slide 9 — Choosing a vector DB (FDE decision)
- "Data must stay in our AWS?" → OpenSearch / Bedrock KB
- "Already on Postgres?" → pgvector
- "SaaS ok, move fast?" → Pinecone
- "Local POC?" → ChromaDB

**Speaker notes:** This decision tree is gold in interviews and real engagements. Tie each to a customer constraint, not a preference.

---

### Slide 10 — Building ingestion
- Load docs → chunk → add to collection
- Store text + metadata (source!)
- Metadata enables citations + filters

**Speaker notes:** Show `ingest_documents()` in `../lab/src/ingest/rag.py`. Note we store `source` so answers can cite the doc.

---

### Slide 11 — Retrieval
- Embed the query
- `collection.query(..., n_results=3)`
- Return chunks + sources + scores

**Speaker notes:** Show `search_documents()`. Top-k retrieval. Discuss tuning k: too low misses context, too high adds noise/cost.

---

### Slide 12 — Assembling the prompt
- System prompt sets rules (answer only from context)
- Inject retrieved chunks as context
- Instruct: cite sources, say "I don't know" if absent

**Speaker notes:** Show `SYSTEM_PROMPT` in `../lab/src/agent/prompts.py`. The "only answer from context" rule is your anti-hallucination guardrail.

---

### Slide 13 — Prompt engineering for reliability
- Be explicit about boundaries
- Demand citations
- Low temperature for factual tasks
- Tell it what to do when unsure

**Speaker notes:** Reliability > cleverness in enterprise. A boring, predictable assistant that cites sources beats a creative one that guesses.

---

### Slide 14 — From RAG to Agents
- RAG = knowledge
- Agent = knowledge + actions
- Agent decides WHEN to call tools

**Speaker notes:** Transition. Our pilot also needs to look up live order status — that's an action, not a document. Enter tools.

---

### Slide 15 — Tool use / function calling
- Define tools with JSON schema
- LLM emits a tool call → you run it → feed result back
- LLM composes final answer

**Speaker notes:** Show `TOOL_DEFINITIONS` in `tools.py` and the tool-calling loop in `support_agent.py`. The order tool from Ch 3 is now LLM-callable.

---

### Slide 16 — Agentic RAG pattern
- One assistant: searches docs AND calls order API
- Picks the right capability per question
- This is what real support assistants do

**Speaker notes:** RetailCo: "What's your return policy?" → RAG. "Status of ORD-1001?" → tool. Same assistant. Reference the agentic pattern in the architectures doc.

---

### Slide 17 — Mock mode (no API key)
- `MOCK_LLM=true` → keyword logic, no LLM call
- Demo anywhere, even offline
- Passes security review before LLM approval

**Speaker notes:** Show `_mock_response()` in `support_agent.py`. This is an FDE superpower: demo the architecture and flow before the customer approves sending data to an LLM.

---

### Slide 18 — Provider flexibility
- OpenAI for speed of dev
- Bedrock to keep data in customer AWS
- Same code path, swap config

**Speaker notes:** Show how `support_agent.py` branches on config. Customers in regulated industries will demand Bedrock/in-VPC — be ready to swap.

---

### Slide 19 — Evaluating the pilot
- Build a test set (RetailCo: 15 Q&A)
- Measure: retrieval recall, answer correctness, latency
- Tools: RAGAS, LLM-as-judge, simple asserts

**Speaker notes:** Don't skip eval — it's how you PROVE value at demo day. Show the minimal eval pattern (must_contain assertions). Target: 80%.

---

### Slide 20 — What we built
- Ingestion pipeline (chunk→embed→store)
- RAG retrieval with citations
- Agent with tool use (order lookup)
- Mock mode + provider flexibility
- An eval harness

**Speaker notes:** Recap. The pilot now has a brain. Next chapter: deploy it, demo it, hand it off.

---

## Demo (Instructor-led): Add the AI Brain

**Goal:** Turn the Ch 3 skeleton into a RAG + agent assistant.

**Walkthrough script:**

1. Open `../lab/src/ingest/rag.py` — explain chunk → embed → store; run `python -m src.ingest.rag` and show "Indexed N chunks."
2. Open `../lab/src/agent/prompts.py` — walk the system prompt rules.
3. Open `../lab/src/agent/support_agent.py` — walk:
   - retrieval (`search_documents`)
   - mock path (`_mock_response`)
   - real LLM path with tool-calling loop
4. Start the server (`MOCK_LLM=true` first):
   ```bash
   cd ../lab && source .venv/bin/activate
   uvicorn src.api.main:app --reload --port 8000
   ```
5. In the UI/`/docs`, ask:
   - "What is the return policy?" → cites `returns-policy.md`
   - "Status of ORD-1001?" → calls `lookup_order` tool
6. (Optional) Set `MOCK_LLM=false` + `OPENAI_API_KEY`, restart, show real LLM answering with the same flow.
7. Run `./scripts/demo.sh` to show all 4 eval questions passing.

**Takeaway:** Same architecture works in mock mode (free, offline) and with a real LLM — perfect for demos and security reviews.

---

## Hands-On Exercise

**Title:** Improve the RAG and add an eval

**Instructions for students:**
1. Add a new policy doc (e.g., `price-match-policy.md`) to `../lab/data/docs/`.
2. Re-run ingestion; verify the assistant answers a price-match question with a citation.
3. Add 3 new questions to a small eval list with `must_contain` assertions.
4. (Stretch) Tune `n_results` and chunk size; observe answer quality.

**Deliverable:** New doc indexed + assistant answering correctly + 3-question eval.

**Solution notes (instructor):** Verify the citation points to the new doc. Good students notice retrieval pulling the right source. Stretch: discuss recall vs noise when changing k.

---

## Quiz (6 questions)

1. When do you choose RAG over fine-tuning? *(changing knowledge, need citations, fast updates)*
2. What does an embedding represent? *(semantic meaning as a vector; similar text = close vectors)*
3. Name the steps of the ingestion pipeline. *(load → chunk → embed → store)*
4. What makes a system "agentic" vs plain RAG? *(LLM decides when to call tools/actions)*
5. Why is mock mode valuable to an FDE? *(demo without keys/data; pass security review before LLM approval)*
6. Pick a vector DB for "data must stay in our AWS account" and justify. *(OpenSearch Serverless or Bedrock KB — in-VPC, IAM)*

---

## Downloadable Resources

- RAG deep-dive → `../docs/vector-dbs-and-rag-architectures.md`
- Ingestion code → `../lab/src/ingest/rag.py`
- Agent + tools → `../lab/src/agent/`
- Prompts → `../lab/src/agent/prompts.py`

## Instructor Tips

- This is your flagship chapter — invest most production polish here.
- Demo mock mode first (always works), then real LLM as the "wow."
- Sell the vector-DB decision tree as an interview cheat code.
