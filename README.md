# Agentic IT Support Ticket Router

## Problem

Customer support teams are overwhelmed with tickets that could be automatically resolved or properly routed, leading to slow response times and poor customer satisfaction.

## Objective

Build an AI agent that analyzes incoming support tickets, extracts key information, checks knowledge bases, and either resolves the ticket automatically or routes it to the appropriate specialist with context.

## Components

**Ticket Classification**: Use LangChain to classify tickets by urgency, department, and complexity

**Knowledge Base RAG**: Vector store with company documentation, FAQs, and past ticket resolutions

**LangGraph Workflow**: Multi-step decision tree that attempts self-resolution before escalation

**Integration Points**: Email/Zendesk/Slack APIs for ticket ingestion

**Human-in-the-Loop**: Escalation mechanism with confidence scoring

## Tech Stack

* Python
* LangChain
* LangGraph
* ChromaDB/Pinecone
* FastAPI
* React dashboard

## System Architecture

![alt text](./images/ITSupportSystemsArchitecture.png)

* Ticket
* Detector
* Classifier
* RAG Retrieval 
* Resolver
* Verifier
* Decision

## Project Structure
```
.
├── README.md
├── agents
│   ├── classifier.py
│   ├── detector.py
│   ├── resolver.py
│   └── router.py
├── apps
├── data
│   ├── load_raw_csv.py
│   └── tickets
│       ├── customer_support_tickets.csv
│       └── tickets_private.csv
├── docs
├── main.py
├── outputs
├── rag
│   ├── chunking.py
│   ├── embeddings.py
│   ├── indexKB.py
│   ├── indexTickets.py
│   ├── loadKB.py
│   ├── prompts.py
│   ├── retrieve.py
│   ├── utils.py
│   └── vectorDB.py
├── schemas
│   ├── decision.py
│   ├── evidence.py
│   ├── resolution.py
│   ├── ticket.py
│   └── triage.py
├── scripts
└── tests
```


## References

Aniket Hingane. “Building an Intelligent Customer Support System with Multi-Agent Architecture.” DEV Community, 28 Dec. 2025, dev.to/exploredataaiml/building-an-intelligent-customer-support-system-with-multi-agent-architecture-236h. 