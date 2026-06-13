---
marp: true
theme: mlopsguru
paginate: true
---


<!-- _class: lead -->

# FDE101 Bonus Module B — Deploy for Azure Customers

## FDE101 · mlopsguru

---

# Welcome

- FDE101 Bonus B: Deploy for Azure Customers
- "OpenAI models, in their tenant"

<!-- For Microsoft-aligned enterprises. The hook: customers get the OpenAI models they want, but inside Azure with their compliance and Entra identity. -->


---

# When you reach for Azure

- Microsoft enterprise (M365, Entra, Azure)
- Compliance/regulatory posture
- Want OpenAI models in-tenant

<!-- These surface in discovery. Many large/regulated enterprises are Azure-first because of existing Microsoft agreements. -->


---

# The Azure architecture

- App Gateway → Container Apps → Azure OpenAI + AI Search
- Key Vault, Entra ID, App Insights
- All in the customer's subscription/VNet

<!-- Walk the diagram. Emphasize in-tenant data and Entra identity as the Azure differentiators. -->


---

# Compute: Container Apps vs AKS

- Container Apps: serverless, scale-to-zero, simplest
- AKS: full Kubernetes, only if they demand it
- App Service: alternative for simple web apps

<!-- Default to Container Apps for pilots. AKS is overkill unless the customer already runs K8s. -->


---

# Images with ACR

- Build → push to ACR
- Entra-integrated access control
- Image scanning via Defender for Cloud

<!-- ACR is the private registry. Defender for Cloud adds vulnerability scanning — a security-team plus. -->


---

# LLM: Azure OpenAI Service

- Same GPT-4o models, Azure-hosted
- Data stays in tenant; not used for training
- Deployments + content filters

<!-- Centerpiece. Show how the swappable LLM design means just changing endpoint/credentials. Mention content filtering as a built-in safety control. -->


---

# Embeddings: Azure OpenAI

- text-embedding-3-small/large deployments
- In-tenant embeddings
- Re-embed when changing models

<!-- Same re-ingest rule. Embeddings and LLM both via Azure OpenAI deployments. -->


---

# Vector store: Azure AI Search

- Vector + keyword (BM25) + semantic ranker
- Managed index, scales easily
- Integrated security with Entra

<!-- Direct ChromaDB upgrade. The semantic ranker (reranking) is a built-in quality boost — tie to Ch 4 reranking pattern. -->


---

# Fastest path: "on your data"

- Azure AI Search + Azure OpenAI "on your data"
- Built-in RAG orchestration
- Less control, faster pilot

<!-- The managed RAG option — analogous to Bedrock KB on AWS. Good for speed-first pilots. -->


---

# Secrets: Azure Key Vault

- No secrets in env/images
- Managed identity reads at runtime
- Keys, secrets, certificates

<!-- Contrast with local `.env`. Key Vault + managed identity = no credentials in code. -->


---

# Identity: Microsoft Entra ID

- Managed identity = app's identity (no secrets)
- Entra SSO = agent login
- Native to Microsoft customers

<!-- This is Azure's biggest enterprise advantage. Managed identity replaces stored credentials; Entra is already the customer's identity system. -->


---

# Networking

- VNet + private subnets
- Application Gateway (WAF) for ingress/TLS
- Private Endpoints for OpenAI/Search

<!-- Keep traffic on the VNet via Private Endpoints. WAF on App Gateway is a security-review winner. -->


---

# Observability

- Application Insights: traces, requests, dependencies
- Azure Monitor: metrics + alerts
- Reuse /health + custom metrics

<!-- App Insights gives rich tracing with little code. Wire latency and retrieval-quality metrics. -->


---

# Infrastructure as Code

- Bicep (Azure-native) or Terraform
- Resource groups for clean teardown
- Tag for cost tracking

<!-- Bicep is concise and Azure-native; Terraform if the customer is multi-cloud. Resource groups make teardown trivial. -->


---

# CI/CD

- Azure DevOps Pipelines or GitHub Actions
- Build → ACR → Container Apps revision
- Revisions enable easy rollback

<!-- Container Apps "revisions" give blue/green-style rollouts. Tie to iterative delivery from Ch 3. -->


---

# Cost control (FDE skill)

- Container Apps scale-to-zero between demos
- Azure OpenAI: GPT-4o-mini for cost
- AI Search tier sizing (free/basic for pilot)
- Delete resource group when idle

<!-- Scale-to-zero is a real cost win for pilots. AI Search has a free tier suitable for small pilots. -->


---

# Security posture summary

- Data in tenant (Azure OpenAI + AI Search)
- Entra managed identity, Key Vault secrets
- Private Endpoints, WAF, encryption
- Microsoft Purview for governance (optional)

<!-- The Azure security answer sheet. Entra + compliance certifications are why regulated customers pick Azure. -->


---

# Topic: Multi-Agent Orchestration on Azure

- One agent → a **team of specialized agents** coordinated by an orchestrator
- When to use: workflows too broad for a single prompt/toolset
- RetailCo example: an **orchestrator** routes "policy" questions → **RAG agent**, "order" questions → **order-lookup agent**, "warranty claims" → **claims agent**
- Benefits: separation of concerns, per-agent prompts/tools/content-filters, easier eval

<!-- Same motivation as the other clouds — single mega-prompt gets brittle as pilots grow. Microsoft has the richest first-party agent tooling, so this lands especially well with Azure customers. Use the RetailCo split as the running example. -->


---

# Azure services for multi-agent

- **Azure AI Foundry Agent Service**: managed agents with **connected/multi-agent** workflows
- **Semantic Kernel**: Microsoft's orchestration SDK — agents, planners, plugins (multi-agent supported)
- **AutoGen**: Microsoft Research multi-agent conversation framework (great for prototyping agent teams)
- **Azure Durable Functions**: stateful, auditable orchestration with human-approval steps
- **Observability**: Application Insights traces + Azure Monitor; tag spans per agent

<!-- Map options to control level. AI Foundry Agent Service = managed/fastest, native to Azure. Semantic Kernel = production code-first orchestration in .NET/Python. AutoGen = rapid multi-agent experimentation. Durable Functions = deterministic, auditable workflows with human-in-the-loop — important for APRA/finance customers. Stress per-agent tracing in App Insights for debugging, cost, and audit. -->


---

# What we deployed

- Pilot live in customer Azure subscription
- Azure OpenAI + AI Search RAG
- Entra identity, secure, observable
- Production-ready foundation



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


## Hands-On Exercise

**Title:** Azure deployment plan + Azure OpenAI swap

**Instructions for students:**
1. Write a one-page Azure deployment plan for RetailCo: services, VNet, Entra identity, cost estimate.
2. Update the pilot's LLM provider switch so `LLM_PROVIDER=azure_openai` is documented (endpoint + deployment + managed identity auth).
3. Choose: Azure AI Search vs Cosmos DB for PostgreSQL (pgvector) — justify for a 2-week pilot.
4. (Stretch) Write the Bicep for ACR + one Container App with managed identity.

**Deliverable:** Deployment plan + provider-swap notes + vector-store decision with justification.

**Solution notes (instructor):** Reward managed identity (no stored secrets), Private Endpoints, scale-to-zero for cost, and using AI Search's semantic ranker as a reranking step.


## Quiz (7 questions)

1. Why do Microsoft enterprises prefer Azure OpenAI over public OpenAI? *(same models, in-tenant data + compliance + Entra)*
2. When choose Container Apps vs AKS? *(Container Apps = serverless/simplest; AKS = full K8s if mandated)*
3. Which Azure service provides vector + keyword + semantic ranking? *(Azure AI Search)*
4. What does a managed identity remove the need for? *(stored credentials/secrets in the app)*
5. What does a Private Endpoint achieve? *(keeps OpenAI/Search traffic on the VNet, off the internet)*
6. Name two cost levers in this stack. *(scale-to-zero; GPT-4o-mini; AI Search tier; delete resource group)*
7. Name two Azure options for multi-agent orchestration and when you'd pick each. *(AI Foundry Agent Service = managed/fast; Semantic Kernel = production code-first; AutoGen = prototyping; Durable Functions = deterministic/auditable with human-in-the-loop)*


## Cost & Security Notes

- **Cost:** Container Apps scale-to-zero (cheap idle), Azure OpenAI per-token, AI Search has a free/basic tier for pilots. Delete the resource group to stop all spend.
- **Security:** In-tenant data, Entra managed identity, Key Vault, Private Endpoints, App Gateway WAF, encryption at rest/in transit, optional Purview governance.

## Downloadable Resources

- RAG/vector deep-dive → `../../../docs/vector-dbs-and-rag-architectures.md`
- Local deployment runbook → `../../../lab/deliverables/deployment-runbook.md`
- Lab Dockerfile → `../../../lab/Dockerfile`

<!-- Recap. Same Core Track app, now enterprise-deployed on Azure. -->


---
