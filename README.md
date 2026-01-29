# Agentic IT Support Ticket Router

## Problem

Customer support teams are overwhelmed with tickets that could be automatically resolved or properly routed, leading to slow response times and poor customer satisfaction.

## Objective

Build an AI agent that analyzes incoming support tickets, extracts key information, checks knowledge bases, and either resolves the ticket automatically or routes it to the appropriate specialist with context.

* AUTO_RESOLVE

* ESCALATE

* ASK_CLARIFYING

## Components

**Ticket Classification**: Use LangChain to classify tickets by urgency, department, and complexity (_IN PROGRESS_ - Currently NOT Using LangChain)

**Knowledge Base RAG**: Vector store with company documentation, FAQs, and past ticket resolutions (_IN PROGRESS_ - Currently using baseline, NOT vector store)

**LangGraph Workflow**: Multi-step decision tree that attempts self-resolution before escalation (_COMPLETE_)

**Integration Points**: Email/Zendesk/Slack APIs for ticket ingestion (_PLANNED_)

**Human-in-the-Loop**: Escalation mechanism with confidence scoring (_COMPLETE_)


## Tech Stack

* Python
* LangChain
* LangGraph
* ChromaDB/Pinecone
* FastAPI
* React dashboard


## Dataset

Tickets are loaded from data/tickets/customer_support_tickets.csv


## System Architecture

![alt text](./images/ITSupportSystemsArchitecture.png)

Pipeline: 
- **Ticket**
- **Detector**
- **Classifier**
- **RAG Retrieval** 
- **Resolver**
- **Verifier**
- **Decision**

## Project Structure
```
.
├── README.md
├── agents
│   ├── __init__.py
│   ├── agenticClassifier.py
│   ├── agenticDetector.py
│   ├── agenticResolver.py
│   ├── agenticRouter.py
│   └── agenticVerifier.py
├── apps
├── data
│   ├── KB
│   ├── __init__.py
│   ├── load_raw_csv.py
│   └── tickets
│       ├── customer_support_tickets.csv
│       └── tickets_private.csv
├── docs
├── images
│   └── ITSupportSystemsArchitecture.png
├── main.py
├── outputs
│   ├── chroma_db
│   │   └── chroma.sqlite3
│   └── runs
│       ├── replay_20260128_001329.jsonl
│       ├── ...
├── rag
│   ├── __init__.py
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
│   ├── __init__.py
│   ├── decision.py
│   ├── detector.py
│   ├── evidence.py
│   ├── resolution.py
│   ├── ticket.py
│   ├── triage.py
│   └── verifier.py
├── scripts
│   ├── eval_run.py
│   ├── replay.py
│   └── seedKB.py
└── tests
```


## References

Aniket Hingane. “Building an Intelligent Customer Support System with Multi-Agent Architecture.” DEV Community, 28 Dec. 2025, dev.to/exploredataaiml/building-an-intelligent-customer-support-system-with-multi-agent-architecture-236h. 