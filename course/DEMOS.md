# FDE101 — All Demos (Compiled)

Instructor-led demo walkthroughs extracted from every chapter and bonus module.

> Note: demos reference a `lab/` RetailCo pilot project that is not currently in this repo. Ask to regenerate it if needed.


---

## Source: Chapter 1 — The Forward Deployed Engineer Role & Mindset

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


---

## Source: Chapter 2 — Customer Discovery & Scoping

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


---

## Source: Chapter 3 — Rapid Prototyping & Customer Integration

## Demo (Instructor-led): Build the API

**Goal:** Go from empty folder to running, demoable API.

**Walkthrough script:**

1. Show the repo structure in `../lab/`.
2. Open `src/api/main.py` — explain FastAPI app, models, endpoints.
3. Open `src/agent/tools.py` — explain `lookup_order` (mock now, HTTP later) and `extract_order_id`.
4. Run setup:
   ```bash
   cd ../lab
   cp .env.example .env
   ./scripts/setup.sh
   source .venv/bin/activate
   uvicorn src.api.main:app --reload --port 8000
   ```
5. Open `http://localhost:8000/docs`, call `/health`, then `/chat` with `"status of ORD-1001?"`.
6. Run `./scripts/demo.sh` to show the automated happy path.
7. Open `http://localhost:8000` to show the chat UI.

**Takeaway:** A working, demoable pilot backend in under an hour — without any real customer access yet.

---


---

## Source: Chapter 4 — AI/LLM Integration: RAG & Agents

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


---

## Source: Chapter 5 — Deploy, Demo & Handoff

## Demo (Instructor-led): Deploy + Present

**Goal:** Containerize, run prod-like, and deliver the closing demo.

**Walkthrough script:**

1. Show `../lab/Dockerfile` and `docker-compose.yml`.
2. Deploy:
   ```bash
   cd ../lab
   docker compose up --build -d
   docker compose logs -f api
   curl http://localhost:8000/health
   ```
3. Walk the deployment runbook (`deliverables/deployment-runbook.md`), including the AWS production section.
4. Switch hats to "demo day": follow `deliverables/demo-script.md` end-to-end against the running container.
5. Show the handoff checklist (`../templates/handoff-checklist.md`) as the closing deliverable.

**Takeaway:** From laptop to deployed, demoed, and handed-off — a complete engagement.

---


---

## Source: FDE101 Bonus Module A — Deploy for AWS Customers

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


---

## Source: FDE101 Bonus Module B — Deploy for Azure Customers

## Demo (Instructor-led): Deploy to Azure

> **Note:** Requires an Azure subscription with Azure OpenAI access approved. If teaching without live Azure, present the IaC/CLI + portal screenshots and run the local pilot alongside to show identical behavior.

**Walkthrough script:**

1. Create registry and push image:
   ```bash
   cd ../../lab
   az group create -n retailco-pilot-rg -l australiaeast
   az acr create -g retailco-pilot-rg -n retailcopilotacr --sku Basic
   az acr login -n retailcopilotacr
   docker build -t retailcopilotacr.azurecr.io/retailco-pilot:latest .
   docker push retailcopilotacr.azurecr.io/retailco-pilot:latest
   ```
2. Show the Azure OpenAI swap concept (config-driven endpoint + deployment name); same `/chat` flow.
3. Deploy to Container Apps:
   ```bash
   az containerapp env create -g retailco-pilot-rg -n retailco-env -l australiaeast
   az containerapp create -g retailco-pilot-rg -n retailco-pilot \
     --environment retailco-env \
     --image retailcopilotacr.azurecr.io/retailco-pilot:latest \
     --target-port 8000 --ingress external \
     --env-vars LLM_PROVIDER=azure_openai VECTOR_BACKEND=azure_search
   ```
4. Hit the Container App URL `/health`, then `/chat` with the RetailCo questions.
5. Show Application Insights traces + Key Vault holding secrets.

**Reference Bicep (teaching snippet — adapt to the customer subscription):**

```bicep
// Azure Container App running the pilot (abridged for teaching)
param location string = resourceGroup().location

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: 'retailco-env'
  location: location
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: 'retailco-pilot'
  location: location
  identity: { type: 'SystemAssigned' }   // managed identity → Key Vault, OpenAI
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      ingress: { external: true, targetPort: 8000 }
      registries: [ { server: 'retailcopilotacr.azurecr.io', identity: 'system' } ]
    }
    template: {
      containers: [ {
        name: 'api'
        image: 'retailcopilotacr.azurecr.io/retailco-pilot:latest'
        env: [
          { name: 'LLM_PROVIDER', value: 'azure_openai' }
          { name: 'AZURE_OPENAI_DEPLOYMENT', value: 'gpt-4o-mini' }
          { name: 'VECTOR_BACKEND', value: 'azure_search' }
        ]
        resources: { cpu: json('0.5'), memory: '1Gi' }
      } ]
      scale: { minReplicas: 0, maxReplicas: 3 }   // scale-to-zero for cost
    }
  }
}
```

**Takeaway:** Same pilot, now running in the customer's Azure subscription with data kept in-tenant.

---


---

## Source: FDE101 Bonus Module C — Deploy for GCP Customers

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

