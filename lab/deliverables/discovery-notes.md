# Discovery Notes — RetailCo

**Date:** 2026-06-01
**FDE:** Praveen Mali
**Validated by:** Sarah Chen (Support Director)

## Pain Summary

RetailCo support team drowning in repeat questions. 400+ tickets/day, 4.2hr first response. Previous chatbot failed because it couldn't use internal docs or look up orders.

## Scoped Pilot

| In | Out |
|----|-----|
| Internal agent-facing assistant | Customer-facing chatbot |
| 3 policy doc sets (ship/return/warranty) | Full Confluence migration |
| Order lookup via sandbox API | Production order write access |
| Local/AWS sandbox deploy | Production VPC (Phase 2) |

## Success Metrics Agreed

1. 80% accuracy on 15-question eval set
2. Order lookup < 3 seconds
3. 3-day agent trial with 15 agents

## Technical Decisions

- **RAG** over fine-tuning — docs change frequently, need citations
- **ChromaDB** for pilot — swap to OpenSearch for production (customer preference)
- **Mock LLM mode** for security review before OpenAI/Bedrock approval
- **FastAPI** — easy for customer IT to maintain post-handoff

## Risks Log

| Risk | Status |
|------|--------|
| Security review of LLM data flow | In progress — James Okonkwo |
| Order API rate limits | Sandbox: 100 req/min — sufficient for pilot |
| Agent adoption | Sarah scheduling 30-min training session |

## Next Steps

- [x] Week 1: Core RAG + order tool
- [ ] Week 2: Agent trial + demo to Sarah
- [ ] Week 3: Security sign-off for production LLM
- [ ] Week 4: Handoff or expand scope
