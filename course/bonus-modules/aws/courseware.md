# FDE101 Bonus Module A — Deploy for AWS Customers

**Duration:** ~90 minutes
**Format:** 18 slides + 1 demo (deploy to AWS) + 1 exercise + quiz
**Prerequisite:** Completed Core Track (Chapters 1–5); pilot runs locally.

---

## Module Overview

Take the RetailCo pilot and deploy it into a customer's **AWS account** using managed, FDE-relevant services. The key win: **Amazon Bedrock keeps customer data inside their AWS account** — no data leaves to public LLM APIs, which is what unblocks enterprise security reviews.

## Learning Objectives

By the end, students can:

1. Map each pilot component to the right AWS service
2. Deploy the container to ECS Fargate (or App Runner) from ECR
3. Swap OpenAI → Amazon Bedrock and ChromaDB → OpenSearch Serverless (or Bedrock Knowledge Bases)
4. Wire secrets, identity, networking, and observability the AWS way
5. Explain the cost and security posture to a customer

---

## Why AWS (customer signals)

- Customer says "everything must stay in our AWS account / our region"
- Heavy existing AWS footprint (ECS/EKS, S3, IAM)
- Security team requires VPC isolation + IAM-based access
- Your own background (Tabcorp ECS/EKS, Terraform) makes this the strongest module to demo

---

## Architecture on AWS

```
                         ┌─────────────────────────── Customer AWS Account ───────────────────────────┐
                         │                                                                             │
   Support agents ──▶ Route 53 ──▶ ALB ──▶ ECS Fargate (FastAPI container from ECR)                    │
                         │                          │                                                  │
                         │                          ├─▶ Amazon Bedrock (Claude)      ← LLM (in-VPC)    │
                         │                          ├─▶ Bedrock Titan Embeddings     ← embeddings      │
                         │                          ├─▶ OpenSearch Serverless (k-NN) ← vector store    │
                         │                          ├─▶ Secrets Manager              ← API keys        │
                         │                          └─▶ Order API / RDS              ← customer data    │
                         │                                                                             │
                         │   Observability: CloudWatch Logs + Metrics + X-Ray      IaC: Terraform/CDK  │
                         └─────────────────────────────────────────────────────────────────────────────┘
```

---

## Service-by-Service Mapping

| Pilot component | Local | AWS service | Why this service |
|-----------------|-------|-------------|------------------|
| Run container | Docker | **ECS Fargate** (or **App Runner** for simplest) | Serverless containers, no EC2 to manage; Fargate for VPC control, App Runner for speed |
| Image registry | local | **Amazon ECR** | Private, IAM-controlled image storage |
| LLM | OpenAI | **Amazon Bedrock** (Claude 3 Haiku/Sonnet) | Data stays in AWS; no public API egress |
| Embeddings | Chroma default | **Bedrock Titan Text Embeddings v2** | In-account embeddings, pairs with Bedrock |
| Vector store | ChromaDB | **OpenSearch Serverless (k-NN)** | Managed ANN + hybrid search; IAM + VPC |
| Managed RAG (alt) | — | **Bedrock Knowledge Bases** | Fully managed ingest+retrieve from S3 — fastest path |
| Relational/orders | orders.json | **RDS / Aurora** (or existing order API) | Real customer data source |
| Secrets | `.env` | **AWS Secrets Manager** | Rotated, IAM-scoped secrets |
| Identity | none | **IAM roles** (task role) + **Cognito** (user auth) | Least-privilege; agent SSO |
| Network/ingress | localhost | **VPC** + **ALB** + private subnets | Isolation + TLS termination |
| Private access to AWS APIs | — | **VPC endpoints / PrivateLink** | Keep Bedrock/OpenSearch traffic off the internet |
| Observability | console | **CloudWatch** (logs/metrics) + **X-Ray** (tracing) | Ops visibility = customer trust |
| IaC | none | **Terraform** or **AWS CDK** | Repeatable, reviewable deploys |
| CI/CD | scripts | **CodePipeline** or **GitHub Actions → ECR/ECS** | Iterative pilot releases |

---

## Slide Deck (slide-by-slide)

### Slide 1 — Title
- FDE101 Bonus A: Deploy for AWS Customers
- "Keep the data in their account"

**Speaker notes:** This module is for AWS customers. The headline benefit is data residency via Bedrock. Frame it as the enterprise-unblocking module.

---

### Slide 2 — When you reach for AWS
- Customer mandate: stay in our AWS/region
- Existing AWS footprint
- Security wants VPC + IAM

**Speaker notes:** Tie back to discovery (Ch 2) — these signals surface in the technical landscape questions.

---

### Slide 3 — The AWS architecture
- ALB → ECS Fargate → Bedrock + OpenSearch
- Secrets Manager, IAM, CloudWatch
- All in the customer VPC

**Speaker notes:** Walk the architecture diagram. Emphasize nothing leaves the account — Bedrock and OpenSearch are in-region, accessed via VPC endpoints.

---

### Slide 4 — Compute: ECS Fargate vs App Runner
- App Runner: simplest, push image → URL
- ECS Fargate: full VPC/network control
- EKS: only if customer already runs K8s

**Speaker notes:** Default to App Runner for a fast pilot, Fargate when security needs VPC control. EKS only if they demand it (your Tabcorp experience applies).

---

### Slide 5 — Images with ECR
- Build → tag → push to ECR
- IAM controls who can pull
- Scan images for vulnerabilities

**Speaker notes:** ECR is the private registry. Mention image scanning — security teams love it.

---

### Slide 6 — LLM: Amazon Bedrock
- Managed access to Claude, Titan, etc.
- Data not used for training, stays in region
- Swap OpenAI client → Bedrock client

**Speaker notes:** This is the centerpiece. Show how the swappable LLM design from Ch 4 means only the provider call changes.

---

### Slide 7 — Embeddings: Titan
- Bedrock Titan Text Embeddings v2
- Consistent in-account embeddings
- Re-embed docs when switching models

**Speaker notes:** Remind: change embedding model = re-ingest everything. Match ingest and query embeddings.

---

### Slide 8 — Vector store: OpenSearch Serverless
- Managed k-NN + hybrid (BM25 + vector)
- IAM + VPC access
- Scales without node management

**Speaker notes:** Direct upgrade from ChromaDB. Same RAG code, different store. Hybrid search helps with order IDs/SKUs.

---

### Slide 9 — Fastest path: Bedrock Knowledge Bases
- Point at an S3 bucket of docs
- Managed chunk + embed + retrieve
- Less control, fastest pilot

**Speaker notes:** Offer the trade-off: KB = speed, OpenSearch = control. For a 2-week pilot, KB can be the right call.

---

### Slide 10 — Secrets: Secrets Manager
- No secrets in env files or images
- IAM-scoped, rotatable
- App reads at runtime

**Speaker notes:** Contrast with the local `.env`. Production never ships secrets in images.

---

### Slide 11 — Identity: IAM + Cognito
- Task IAM role = least privilege for the app
- Cognito = support-agent login/SSO
- Map to customer's identity provider

**Speaker notes:** Two layers: the app's permissions (IAM task role) and the users' auth (Cognito/SSO). Your IAM background is the asset.

---

### Slide 12 — Networking
- VPC, private subnets for the app
- ALB for TLS + routing
- VPC endpoints for Bedrock/OpenSearch

**Speaker notes:** Keep traffic private. VPC endpoints mean Bedrock/OpenSearch calls never traverse the internet — a security-review winner.

---

### Slide 13 — Observability
- CloudWatch logs + custom metrics (latency, retrieval quality)
- X-Ray traces across the request
- Alarms wired to runbook

**Speaker notes:** Reuse the `/health` endpoint and add metrics. SRE habits build customer confidence.

---

### Slide 14 — Infrastructure as Code
- Terraform or CDK for every resource
- Reviewable, repeatable, tear-down-able
- Tag everything (owner, cost center)

**Speaker notes:** IaC is how you redeploy in another account cleanly. Show the reference snippet in the demo.

---

### Slide 15 — CI/CD
- GitHub Actions or CodePipeline
- Build → push ECR → deploy ECS
- One pipeline per environment

**Speaker notes:** Iterative pilot releases. Tie to Ch 3 — ship small and often.

---

### Slide 16 — Cost control (FDE skill)
- Fargate right-sized (0.5 vCPU/1GB for pilot)
- Bedrock: pick Haiku for cost, Sonnet for quality
- OpenSearch Serverless OCU minimums — watch idle cost
- Tear down sandbox when idle

**Speaker notes:** Customers watch pilot spend. Know the cost levers. OpenSearch Serverless has a minimum cost — mention KB or pgvector as cheaper alternatives for tiny pilots.

---

### Slide 17 — Security posture summary
- Data stays in account (Bedrock + OpenSearch)
- IAM least privilege, secrets managed
- Private networking, encryption at rest/in transit
- Audit via CloudTrail

**Speaker notes:** This slide is your security-review answer sheet. Walk it as the customer's checklist.

---

### Slide 18 — What we deployed
- Pilot live in customer AWS account
- Bedrock LLM + OpenSearch RAG
- Secure, observable, IaC-managed
- Production-ready foundation

**Speaker notes:** Recap. Same app from the Core Track, now enterprise-deployed on AWS.

---

## Demo (Instructor-led): Deploy to AWS

> **Note:** Requires an AWS account with Bedrock model access enabled. If teaching without live AWS, present the IaC + console screenshots and run the local pilot alongside to show identical behavior.

**Walkthrough script:**

1. Build and push the image:
   ```bash
   cd ../../lab
   aws ecr create-repository --repository-name retailco-pilot
   aws ecr get-login-password | docker login --username AWS --password-stdin <acct>.dkr.ecr.<region>.amazonaws.com
   docker build -t retailco-pilot .
   docker tag retailco-pilot:latest <acct>.dkr.ecr.<region>.amazonaws.com/retailco-pilot:latest
   docker push <acct>.dkr.ecr.<region>.amazonaws.com/retailco-pilot:latest
   ```
2. Show the Bedrock swap concept (config-driven) — the app calls Bedrock instead of OpenAI; same `/chat` flow.
3. Apply reference Terraform (below) to create ECS service, ALB, IAM, Secrets.
4. Hit the ALB URL `/health`, then `/chat` with the same RetailCo questions.
5. Show CloudWatch logs + a metric, and Secrets Manager holding the keys.

**Reference Terraform (teaching snippet — adapt to the customer account):**

```hcl
# ECS Fargate service fronted by an ALB (abridged for teaching)
resource "aws_ecs_cluster" "pilot" {
  name = "retailco-pilot"
}

resource "aws_ecs_task_definition" "app" {
  family                   = "retailco-pilot"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = aws_iam_role.exec.arn
  task_role_arn            = aws_iam_role.task.arn   # least-privilege: Bedrock + OpenSearch + Secrets
  container_definitions = jsonencode([{
    name      = "api"
    image     = "${aws_ecr_repository.pilot.repository_url}:latest"
    portMappings = [{ containerPort = 8000 }]
    environment = [
      { name = "LLM_PROVIDER", value = "bedrock" },
      { name = "BEDROCK_MODEL", value = "anthropic.claude-3-haiku-20240307-v1:0" },
      { name = "VECTOR_BACKEND", value = "opensearch" }
    ]
    secrets = [
      { name = "OPENSEARCH_ENDPOINT", valueFrom = aws_secretsmanager_secret.os.arn }
    ]
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        "awslogs-group"         = "/ecs/retailco-pilot"
        "awslogs-region"        = var.region
        "awslogs-stream-prefix" = "api"
      }
    }
  }])
}

# Task role grants only what the pilot needs
resource "aws_iam_role_policy" "task_perms" {
  role = aws_iam_role.task.id
  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      { Effect = "Allow", Action = ["bedrock:InvokeModel"], Resource = "*" },
      { Effect = "Allow", Action = ["aoss:APIAccessAll"], Resource = "*" },
      { Effect = "Allow", Action = ["secretsmanager:GetSecretValue"], Resource = aws_secretsmanager_secret.os.arn }
    ]
  })
}
```

**Takeaway:** Same pilot, now running in the customer's AWS account with data kept in-region.

---

## Hands-On Exercise

**Title:** AWS deployment plan + Bedrock swap

**Instructions for students:**
1. Write a one-page AWS deployment plan for RetailCo: services, network, IAM, cost estimate.
2. Update the pilot's LLM provider switch so `LLM_PROVIDER=bedrock` is a documented path (pseudo-code or real `boto3` `bedrock-runtime` call).
3. Choose: OpenSearch Serverless vs Bedrock Knowledge Bases — justify for a 2-week pilot.
4. (Stretch) Write the Terraform for ECR + one ECS service.

**Deliverable:** Deployment plan + provider-swap notes + vector-store decision with justification.

**Solution notes (instructor):** Reward least-privilege IAM, VPC endpoints for Bedrock, and a cost-aware vector store choice (KB or pgvector for tiny pilots vs OpenSearch for hybrid/scale).

---

## Quiz (6 questions)

1. What is the main enterprise benefit of Bedrock over public OpenAI? *(data stays in the AWS account/region)*
2. When choose App Runner vs ECS Fargate? *(App Runner = simplest; Fargate = VPC/network control)*
3. Which service stores embeddings for hybrid search? *(OpenSearch Serverless k-NN)*
4. What does a VPC endpoint achieve for Bedrock/OpenSearch traffic? *(keeps it private, off the internet)*
5. Why use an IAM task role instead of embedding credentials? *(least privilege, no secrets in image)*
6. Name two cost levers in this stack. *(Bedrock model choice Haiku vs Sonnet; Fargate sizing; OpenSearch OCU; tear down idle)*

---

## Cost & Security Notes

- **Cost:** Fargate (~small), Bedrock per-token, OpenSearch Serverless has OCU minimums (largest idle cost). For tiny pilots consider Bedrock KB or Aurora pgvector.
- **Security:** Bedrock + OpenSearch in-VPC, IAM least privilege, Secrets Manager, CloudTrail audit, encryption at rest (KMS) and in transit (TLS).

## Downloadable Resources

- RAG/vector deep-dive (AWS options) → `../../../docs/vector-dbs-and-rag-architectures.md`
- Local deployment runbook (production AWS section) → `../../../lab/deliverables/deployment-runbook.md`
- Lab Dockerfile → `../../../lab/Dockerfile`
