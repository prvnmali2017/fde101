# Pilot Plan Template

**Customer:** _______________
**Pilot name:** _______________
**Duration:** 2–4 weeks
**FDE lead:** Praveen Mali

## Executive Summary

_One paragraph: problem, proposed solution, expected outcome._

## Objectives

| # | Objective | Success metric | Owner |
|---|-----------|----------------|-------|
| 1 | | | |
| 2 | | | |
| 3 | | | |

## Scope

### In Scope
-

### Out of Scope
-

## Architecture (high level)

```
[Customer data] → [Ingestion] → [Vector store] → [Agent/API] → [User interface]
                      ↓
              [Customer systems via API]
```

## Timeline

| Week | Milestone | Deliverable |
|------|-----------|-------------|
| 1 | Discovery + setup | Discovery notes, dev environment |
| 2 | Core build | Working API / agent |
| 3 | Integration | Customer system connected |
| 4 | Demo + handoff | Runbook, demo, evaluation results |

## Team & Responsibilities

| Role | Name | Responsibility |
|------|------|----------------|
| FDE (you) | Praveen Mali | Build, deploy, demo |
| Customer sponsor | | Approvals, access |
| Customer technical | | API access, data, testing |

## Risks & Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| API access delayed | High | Start with mock data, swap later |
| Data quality poor | Medium | Limit RAG to curated doc set |
| Security review slow | High | Document architecture early |

## Exit Criteria

Pilot is successful when:
- [ ]
- [ ]
- [ ]

## Post-Pilot Options

1. **Expand** — production deployment, more use cases
2. **Handoff** — customer team takes over with runbook
3. **Pause** — document learnings, revisit later
