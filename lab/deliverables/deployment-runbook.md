# Deployment Runbook — RetailCo Support AI Pilot

**Version:** 0.1
**Environment:** Pilot (local / Docker)
**Owner:** Praveen Mali → RetailCo IT (post-handoff)

## Prerequisites

- Python 3.11+ OR Docker 24+
- `.env` configured (see `.env.example`)
- Network access to LLM provider (if `MOCK_LLM=false`)

## Local Deployment

```bash
cd lab
cp .env.example .env
./scripts/setup.sh
source .venv/bin/activate
uvicorn src.api.main:app --host 0.0.0.0 --port 8000
```

Verify: `curl http://localhost:8000/health`

## Docker Deployment

```bash
cd lab
cp .env.example .env
docker compose up --build -d
docker compose logs -f api
```

Verify: `curl http://localhost:8000/health`

## Re-index Documents

When policy docs in `data/docs/` change:

```bash
source .venv/bin/activate
python -m src.ingest.rag
# Or in Docker:
docker compose exec api python -m src.ingest.rag
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `MOCK_LLM` | Skip LLM API calls | `true` |
| `OPENAI_API_KEY` | OpenAI key | — |
| `OPENAI_MODEL` | Model name | `gpt-4o-mini` |
| `CHROMA_PERSIST_DIR` | Vector store path | `./data/chroma` |

## Production Migration (Phase 2)

For RetailCo AWS (ap-southeast-2):

1. **Compute:** ECS Fargate task (512 CPU / 1024 MB sufficient for pilot)
2. **Vector store:** OpenSearch Serverless with k-NN
3. **LLM:** Amazon Bedrock (Claude 3 Haiku) — data stays in AWS
4. **Secrets:** AWS Secrets Manager for API keys
5. **Network:** Private subnets, ALB with IP allowlist for support office
6. **Monitoring:** CloudWatch metrics + alarms on `/health` and latency

Use your existing Terraform/CDK patterns from Tabcorp — same modules, customer VPC.

## Rollback

```bash
docker compose down
# Or kill uvicorn process
# Previous ChromaDB persists in data/chroma/ — delete to force full re-ingest
```

## Support Contacts

| Issue | Contact |
|-------|---------|
| Application errors | FDE: Praveen Mali |
| Order API | Priya Sharma (E-commerce) |
| Security / access | James Okonkwo (IT Security) |
| Business sign-off | Sarah Chen (Support Director) |
