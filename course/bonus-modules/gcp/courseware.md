# FDE101 Bonus Module C — Deploy for GCP Customers

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (deploy to GCP) + 1 exercise + quiz
**Prerequisite:** Completed Core Track (Chapters 1–5); pilot runs locally.

---

## Module Overview

Take the RetailCo pilot and deploy it into a customer's **Google Cloud project** using managed, FDE-relevant services. The key win: **Vertex AI keeps data in the customer's project/region** with Gemini models, and **Cloud Run** offers the simplest serverless container deployment of the three clouds.

## Learning Objectives

By the end, students can:

1. Map each pilot component to the right GCP service
2. Deploy the container to Cloud Run from Artifact Registry
3. Swap OpenAI → Vertex AI (Gemini) and ChromaDB → Vertex AI Vector Search
4. Wire secrets, identity, networking, and observability the GCP way
5. Explain the cost and security posture to a customer

---

## Why GCP (customer signals)

- Data/AI-forward company (BigQuery, Looker, Vertex AI)
- Already on Google Workspace / GKE
- Wants Gemini models in-project
- Values Cloud Run's simple, fast, pay-per-use serverless containers

---

## Architecture on GCP

```
                  ┌──────────────────────── Customer GCP Project ───────────────────────────────┐
                  │                                                                              │
   Agents ──▶ Cloud Load Balancing ──▶ Cloud Run (FastAPI image from Artifact Registry)         │
                  │                          │                                                   │
                  │                          ├─▶ Vertex AI (Gemini 1.5)        ← LLM (in-project)│
                  │                          ├─▶ Vertex AI text-embeddings      ← embeddings     │
                  │                          ├─▶ Vertex AI Vector Search        ← vector store   │
                  │                          ├─▶ Secret Manager                 ← secrets         │
                  │                          └─▶ Order API / Cloud SQL          ← customer data   │
                  │                                                                              │
                  │   Observability: Cloud Monitoring + Cloud Trace          IaC: Terraform      │
                  │   Identity: Cloud IAM + service accounts                                      │
                  └────────────────────────────────────────────────────────────────────────────────┘
```

---

## Service-by-Service Mapping

| Pilot component | Local | GCP service | Why this service |
|-----------------|-------|-------------|------------------|
| Run container | Docker | **Cloud Run** | Simplest serverless containers; scale-to-zero; pay-per-request |
| Orchestration (scale) | — | **GKE** (Autopilot) | Only if customer standardizes on Kubernetes |
| Image registry | local | **Artifact Registry** | Private, IAM-controlled image storage |
| LLM | OpenAI | **Vertex AI** (Gemini 1.5 Flash/Pro) | Data stays in project/region; Google's frontier models |
| Embeddings | Chroma default | **Vertex AI text-embeddings** (text-embedding-004) | In-project embeddings, pairs with Gemini |
| Vector store | ChromaDB | **Vertex AI Vector Search** | Managed ANN at scale (formerly Matching Engine) |
| Vector store (alt) | — | **AlloyDB / Cloud SQL** (pgvector) | If customer prefers Postgres-native vectors |
| Managed RAG (alt) | — | **Vertex AI RAG Engine** | Managed ingest+retrieve orchestration |
| Relational/orders | orders.json | **Cloud SQL** / existing order API | Real customer data source |
| Secrets | `.env` | **Secret Manager** | IAM-scoped, versioned secrets |
| Identity | none | **Cloud IAM** + service accounts (+ **Identity Platform** for users) | Least privilege; agent SSO |
| Network/ingress | localhost | **VPC** + **Cloud Load Balancing** | Isolation + global TLS LB |
| Private access to APIs | — | **Private Service Connect** / VPC-SC | Keep Vertex traffic private; data exfiltration controls |
| Observability | console | **Cloud Monitoring** + **Cloud Trace** + **Cloud Logging** | Ops visibility |
| IaC | none | **Terraform** | Standard for GCP IaC |
| CI/CD | scripts | **Cloud Build** or **GitHub Actions** | Build → Artifact Registry → Cloud Run |

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- FDE101 Bonus C: Deploy for GCP Customers
- "Gemini in their project, the simple way"

**Speaker notes:** For Google Cloud customers. Hooks: Gemini models in-project + Cloud Run being the easiest serverless container platform.

---

### Slide 2 — When you reach for GCP
- Data/AI-forward (BigQuery, Vertex)
- Google Workspace / GKE shops
- Want Gemini in-project

**Speaker notes:** These surface in discovery. GCP customers are often data-heavy and AI-curious — a great fit for the pilot.

---

### Slide 3 — The GCP architecture
- Cloud LB → Cloud Run → Vertex AI + Vector Search
- Secret Manager, IAM, Cloud Monitoring
- All in the customer's project

**Speaker notes:** Walk the diagram. Emphasize in-project data and Cloud Run simplicity.

---

### Slide 4 — Compute: Cloud Run vs GKE
- Cloud Run: simplest, scale-to-zero, pay-per-use
- GKE Autopilot: managed K8s if mandated
- Cloud Run is the default for pilots

**Speaker notes:** Cloud Run is arguably the easiest container deploy across all three clouds — push image, get HTTPS URL. GKE only if the customer demands Kubernetes.

---

### Slide 5 — Images with Artifact Registry
- Build → push to Artifact Registry
- IAM-controlled pulls
- Vulnerability scanning available

**Speaker notes:** Artifact Registry replaced Container Registry (GCR). IAM controls access; scanning helps security teams.

---

### Slide 6 — LLM: Vertex AI (Gemini)
- Gemini 1.5 Flash (fast/cheap) or Pro (quality)
- Data stays in project/region
- Swap OpenAI client → Vertex SDK

**Speaker notes:** Centerpiece. Show the swappable LLM design: only the client/model call changes. Flash vs Pro is the cost/quality lever.

---

### Slide 7 — Embeddings: Vertex AI
- text-embedding-004
- In-project embeddings
- Re-embed when changing models

**Speaker notes:** Same re-ingest rule. Embeddings + LLM both from Vertex AI.

---

### Slide 8 — Vector store: Vertex AI Vector Search
- Managed ANN at large scale
- Low-latency similarity search
- (Was "Matching Engine")

**Speaker notes:** Direct ChromaDB upgrade for scale. For smaller pilots, AlloyDB/Cloud SQL pgvector can be simpler and cheaper — mention the trade-off.

---

### Slide 9 — Fastest path: Vertex AI RAG Engine
- Managed ingest + retrieve orchestration
- Less to build for a pilot
- Pairs with Gemini

**Speaker notes:** GCP's managed RAG option — analogous to Bedrock KB / Azure "on your data." Good for speed-first pilots.

---

### Slide 10 — Secrets: Secret Manager
- No secrets in env/images
- Service account reads at runtime
- Versioned secrets

**Speaker notes:** Contrast with local `.env`. Service account + Secret Manager = no creds in code.

---

### Slide 11 — Identity: Cloud IAM
- Service account = app identity (least privilege)
- Identity Platform / Workspace SSO for agents
- Workload Identity on GKE

**Speaker notes:** Service accounts are the app's identity. Grant only Vertex + Vector Search + Secret Manager access. Your IAM mindset transfers directly.

---

### Slide 12 — Networking
- VPC + Cloud Load Balancing (global)
- Private Service Connect for Vertex
- VPC Service Controls for exfiltration protection

**Speaker notes:** VPC-SC is a strong GCP security feature — it creates a perimeter preventing data exfiltration. A security-review highlight for regulated customers.

---

### Slide 13 — Observability
- Cloud Trace: request tracing
- Cloud Monitoring: metrics + alerts
- Cloud Logging: structured logs

**Speaker notes:** The operations suite (formerly Stackdriver). Reuse `/health` + custom metrics for latency/retrieval quality.

---

### Slide 14 — Infrastructure as Code
- Terraform (standard on GCP)
- Per-project or per-env
- Labels for cost tracking

**Speaker notes:** Terraform is the norm. Labels (GCP's tags) enable cost attribution.

---

### Slide 15 — CI/CD
- Cloud Build or GitHub Actions
- Build → Artifact Registry → Cloud Run deploy
- Revisions + traffic splitting for canary

**Speaker notes:** Cloud Run traffic splitting enables easy canary/blue-green. Tie to iterative delivery from Ch 3.

---

### Slide 16 — Cost control (FDE skill)
- Cloud Run scale-to-zero (pay only on requests)
- Gemini Flash for cost, Pro for quality
- Vector Search has index serving cost — pgvector cheaper for tiny pilots
- Delete project/resources when idle

**Speaker notes:** Cloud Run's pay-per-request is excellent for sporadic pilot traffic. Vector Search has standing cost — call out pgvector for small pilots.

---

### Slide 17 — Security posture summary
- Data in project (Vertex + Vector Search)
- IAM least privilege, service accounts, Secret Manager
- VPC-SC perimeter, Private Service Connect, encryption
- Cloud Audit Logs

**Speaker notes:** The GCP security answer sheet. VPC Service Controls is the standout differentiator for data-sensitive customers.

---

### Slide 18 — What we deployed
- Pilot live in customer GCP project
- Vertex AI (Gemini) + Vector Search RAG
- IAM-secured, observable, IaC-managed
- Production-ready foundation

**Speaker notes:** Recap. Same Core Track app, now enterprise-deployed on GCP.

---

## Demo (Instructor-led): Deploy to GCP

> **Note:** Requires a GCP project with Vertex AI API enabled and billing on. If teaching without live GCP, present the IaC/CLI + console screenshots and run the local pilot alongside to show identical behavior.

**Walkthrough script:**

1. Create registry and push image:
   ```bash
   cd ../../lab
   gcloud artifacts repositories create retailco --repository-format=docker --location=australia-southeast1
   gcloud auth configure-docker australia-southeast1-docker.pkg.dev
   docker build -t australia-southeast1-docker.pkg.dev/PROJECT_ID/retailco/pilot:latest .
   docker push australia-southeast1-docker.pkg.dev/PROJECT_ID/retailco/pilot:latest
   ```
2. Show the Vertex AI swap concept (config-driven model/region); same `/chat` flow.
3. Deploy to Cloud Run:
   ```bash
   gcloud run deploy retailco-pilot \
     --image australia-southeast1-docker.pkg.dev/PROJECT_ID/retailco/pilot:latest \
     --region australia-southeast1 --port 8000 --allow-unauthenticated \
     --set-env-vars LLM_PROVIDER=vertex,VERTEX_MODEL=gemini-1.5-flash,VECTOR_BACKEND=vertex_vector_search
   ```
4. Hit the Cloud Run URL `/health`, then `/chat` with the RetailCo questions.
5. Show Cloud Trace + Secret Manager holding secrets.

**Reference Terraform (teaching snippet — adapt to the customer project):**

```hcl
# Cloud Run service running the pilot (abridged for teaching)
resource "google_cloud_run_v2_service" "pilot" {
  name     = "retailco-pilot"
  location = var.region

  template {
    service_account = google_service_account.pilot.email   # least-privilege SA

    scaling {
      min_instance_count = 0   # scale-to-zero for cost
      max_instance_count = 3
    }

    containers {
      image = "${var.region}-docker.pkg.dev/${var.project}/retailco/pilot:latest"
      ports { container_port = 8000 }

      env {
        name  = "LLM_PROVIDER"
        value = "vertex"
      }
      env {
        name  = "VERTEX_MODEL"
        value = "gemini-1.5-flash"
      }
      env {
        name  = "VECTOR_BACKEND"
        value = "vertex_vector_search"
      }
      # secret from Secret Manager
      env {
        name = "ORDER_API_KEY"
        value_source {
          secret_key_ref {
            secret  = google_secret_manager_secret.order_api.secret_id
            version = "latest"
          }
        }
      }
    }
  }
}

# Grant the service account only what the pilot needs
resource "google_project_iam_member" "vertex" {
  project = var.project
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.pilot.email}"
}
```

**Takeaway:** Same pilot, now running in the customer's GCP project with data kept in-region.

---

## Hands-On Exercise

**Title:** GCP deployment plan + Vertex AI swap

**Instructions for students:**
1. Write a one-page GCP deployment plan for RetailCo: services, VPC, IAM/service accounts, cost estimate.
2. Update the pilot's LLM provider switch so `LLM_PROVIDER=vertex` is documented (Vertex SDK call, model, region).
3. Choose: Vertex AI Vector Search vs AlloyDB/Cloud SQL pgvector — justify for a 2-week pilot.
4. (Stretch) Write the Terraform for Artifact Registry + one Cloud Run service with a service account.

**Deliverable:** Deployment plan + provider-swap notes + vector-store decision with justification.

**Solution notes (instructor):** Reward least-privilege service accounts, scale-to-zero Cloud Run, VPC-SC mention for data protection, and choosing pgvector for tiny pilots vs Vector Search for scale.

---

## Quiz (6 questions)

1. What is the data-residency benefit of Vertex AI over public OpenAI? *(data stays in the GCP project/region)*
2. Why is Cloud Run a great default for pilots? *(serverless, scale-to-zero, pay-per-request, simplest)*
3. Which managed service stores vectors at scale on GCP? *(Vertex AI Vector Search)*
4. What identity does a Cloud Run app use to access Vertex/Secrets? *(a least-privilege service account)*
5. What does VPC Service Controls protect against? *(data exfiltration — creates a security perimeter)*
6. Name two cost levers in this stack. *(Cloud Run scale-to-zero; Gemini Flash vs Pro; Vector Search vs pgvector; delete resources)*

---

## Cost & Security Notes

- **Cost:** Cloud Run pay-per-request (cheap idle), Vertex AI per-token/char, Vector Search has standing index serving cost — prefer pgvector for tiny pilots. Delete resources when idle.
- **Security:** In-project data, IAM service accounts, Secret Manager, VPC Service Controls + Private Service Connect, encryption at rest/in transit, Cloud Audit Logs.

## Downloadable Resources

- RAG/vector deep-dive → `../../../docs/vector-dbs-and-rag-architectures.md`
- Local deployment runbook → `../../../lab/deliverables/deployment-runbook.md`
- Lab Dockerfile → `../../../lab/Dockerfile`
