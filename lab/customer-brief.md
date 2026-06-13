# RetailCo Customer Brief

## Company

**RetailCo** is a mid-size Australian retailer (120 stores, ~800 staff) selling homewares and electronics. They use Shopify for e-commerce and Zendesk for support.

## The Problem

- Support team handles **400+ tickets/day**, 60% are repeat questions (shipping, returns, warranties)
- Average first-response time: **4.2 hours** (target: under 1 hour)
- Internal policy docs are scattered across Confluence, PDFs, and Zendesk macros
- Previous chatbot vendor failed — answers were generic and couldn't look up orders

## What They Want

> "An AI assistant our support agents can use internally — it should answer policy questions from our docs and look up order status when given an order ID."

## Constraints

| Constraint | Detail |
|------------|--------|
| Timeline | 2-week pilot |
| Data | Cannot send customer PII to public LLM APIs without review |
| Integration | Order API exists (REST, API key auth) — sandbox available |
| Deployment | Must run in their AWS account (ap-southeast-2) for production; local OK for pilot |
| Users | 15 support agents in pilot |

## Success Criteria

1. Answer 80% of FAQ test questions correctly (15-question eval set)
2. Order lookup returns status in under 3 seconds
3. Support lead signs off after 3-day agent trial

## Stakeholders

| Role | Name | Concern |
|------|------|---------|
| Support Director | Sarah Chen | Ticket deflection, agent adoption |
| IT Security | James Okonkwo | Data residency, API access |
| E-commerce Lead | Priya Sharma | Order API stability |

## Your Mission (as FDE)

Week 1: Discovery (this brief) + build core RAG
Week 2: Integrate order API + demo to Sarah Chen

This lab implements the **Week 1–2 pilot** locally so you can practice the full FDE workflow.
