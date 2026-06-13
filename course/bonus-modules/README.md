# FDE101 — Bonus Cloud Modules

The Core Track (Chapters 1–5) builds and deploys the **RetailCo AI Support Pilot locally** with Docker. These bonus modules take that **exact same pilot** and re-deploy it into a real **customer cloud environment** using each provider's managed, FDE-relevant services.

> **Why this matters for FDEs:** Customers run on AWS, Azure, or GCP. An FDE must deploy the pilot *in the customer's account* — respecting their identity, networking, data residency, and security. These modules teach the cloud-specific "last mile."

---

## How to Choose a Module

Take the module that matches your **target customer or employer**:

- Selling to AWS shops / applying to AWS-heavy companies → **Bonus A (AWS)**
- Selling to Microsoft enterprises / Azure shops → **Bonus B (Azure)**
- Selling to Google Cloud / data-AI shops → **Bonus C (GCP)**

Ambitious students do all three to be cloud-agnostic (a strong interview signal).

---

## The Same Architecture, Three Clouds

Every module deploys the same logical architecture. Only the managed services change.

```
              ┌──────────────────────────────────────────────┐
              │  RetailCo AI Support Pilot (same app code)     │
              │                                                │
  Users ─────▶│  [Container: FastAPI]                         │
              │     ├─ RAG retrieval  ──▶ [Vector store]      │
              │     ├─ LLM call       ──▶ [Managed LLM]       │
              │     └─ order lookup   ──▶ [Customer API/data] │
              └──────────────────────────────────────────────┘
                 secrets, identity, network, observability
```

### Service mapping (the cheat sheet)

| Capability | Local (Core) | AWS (Bonus A) | Azure (Bonus B) | GCP (Bonus C) |
|------------|--------------|---------------|-----------------|---------------|
| **Run the container** | Docker / Compose | ECS Fargate or App Runner | Azure Container Apps | Cloud Run |
| **Orchestration (scale)** | — | EKS | AKS | GKE |
| **Container registry** | local image | Amazon ECR | Azure Container Registry (ACR) | Artifact Registry |
| **LLM** | OpenAI / mock | Amazon Bedrock (Claude) | Azure OpenAI Service | Vertex AI (Gemini) |
| **Embeddings** | Chroma default | Bedrock Titan Embeddings | Azure OpenAI embeddings | Vertex AI text-embeddings |
| **Vector store** | ChromaDB | OpenSearch Serverless / Aurora pgvector / Bedrock KB | Azure AI Search / Cosmos DB for PostgreSQL | Vertex AI Vector Search / AlloyDB pgvector |
| **Managed RAG (optional)** | — | Bedrock Knowledge Bases | Azure AI Search + "on your data" | Vertex AI RAG Engine |
| **Secrets** | `.env` | AWS Secrets Manager | Azure Key Vault | Secret Manager |
| **Identity / auth** | none | IAM + Cognito | Microsoft Entra ID | Cloud IAM + Identity Platform |
| **Networking / ingress** | localhost | VPC + ALB | VNet + Application Gateway | VPC + Cloud Load Balancing |
| **Private network** | — | PrivateLink / VPC endpoints | Private Endpoints | Private Service Connect |
| **Observability** | logs to console | CloudWatch + X-Ray | Azure Monitor + App Insights | Cloud Monitoring + Cloud Trace |
| **IaC** | none | Terraform / CDK | Bicep / Terraform | Terraform |
| **CI/CD** | scripts | CodePipeline / GitHub Actions | Azure DevOps / GitHub Actions | Cloud Build / GitHub Actions |

---

## Module Structure (all three are parallel)

Each `courseware.md` follows the same shape so students can compare clouds easily:

1. Module overview + learning objectives
2. Why this cloud (customer signals)
3. Architecture on this cloud (diagram)
4. Service-by-service mapping (with the "why")
5. Slide deck (slide-by-slide + speaker notes)
6. Demo walkthrough (deploy steps + reference IaC)
7. Hands-on exercise + solution notes
8. Quiz
9. Cost & security notes
10. Downloadable resources

---

## Important Teaching Notes

- **Data residency is the #1 enterprise driver.** Each managed LLM (Bedrock / Azure OpenAI / Vertex) keeps data in the customer's cloud — unlike calling public OpenAI. Lead with this in customer conversations.
- **Swap, don't rewrite.** The Core Track built the app with swappable interfaces (LLM, vector store). These modules prove that design pays off — only config and infra change.
- **IaC is reference, not copy-paste-to-prod.** Snippets teach the resource shape. Students adapt to the customer's account, regions, and policies.
- **Cost awareness is an FDE skill.** Each module includes a cost-control section — customers watch pilot spend closely.

---

## Recommended Order

1. Finish the Core Track (Chapters 1–5) — pilot working locally.
2. Pick the cloud your customer/employer uses.
3. Complete that bonus module's deploy demo + exercise.
4. (Optional) Repeat for the other two clouds to be cloud-agnostic.

Files:
- `aws/courseware.md` — Bonus A: AWS Customers
- `azure/courseware.md` — Bonus B: Azure Customers
- `gcp/courseware.md` — Bonus C: GCP Customers
