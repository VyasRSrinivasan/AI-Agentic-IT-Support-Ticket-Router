# Agentic IT Support Ticket Router

## Problem

Customer support teams are overwhelmed with tickets that could be automatically resolved or properly routed, leading to slow response times and poor customer satisfaction.

Without automation:
- urgent issues are lost 
- humans route tickets manually
- simple tickets take up expensive support time
- unsafe automation risks customer satisfaction

## Objective

Build an AI agent that analyzes incoming support tickets, extracts key information, checks knowledge bases, and either resolves the ticket automatically or routes it to the appropriate specialist with context.

This system is designed as a decision engine rather than a chatbot.
Agents _analyze_ the ticket, _propose_ an action, and a verifier _enforces_ safety rules before automation is allowed.  
Automation only occurs when confidence and grounding conditions are satisfied — otherwise the ticket escalates to a human specialist.

### Decision

- **AUTO_RESOLVE**: automatically generate a grounded response

- **ESCALATE**: route to a human specialist

- **ASK_CLARIFYING**: ask for more/missing information from the user

## Components

**Ticket Classification**: Use LangChain to classify tickets by urgency, department, and complexity (_Currently NOT Using LangChain_)

**Knowledge Base RAG**: Vector store with company documentation, FAQs, and past ticket resolutions (_Currently using baseline, NOT vector store_)

**LangGraph Workflow**: Multi-step decision tree that attempts self-resolution before escalation 

**Integration Points**: Email/Zendesk/Slack APIs for ticket ingestion (_Currently NOT using this_)

**Human-in-the-Loop**: Escalation mechanism with confidence scoring


## Tech Stack

* Python
* LangChain
* LangGraph
* ChromaDB/Pinecone
* FastAPI
* React dashboard


## Dataset

Customer support dataset:

```
data/tickets/customer_support_tickets.csv
```

Used solely as input simulation for replay & testing.
It is NOT intended as an actual production support dataset.

## System Architecture

![alt text](./images/ITSupportSystemsArchitecture.png)

### Pipeline

- **Ticket**: Normalized structured representation of a support ticket
- **Detector**: Early safety & completeness analysis
- **Classifier**: Operational triage of the ticket based on department, urgency, complexity
- **RAG Retrieval**: Retrieves grounded support knowledge and outputs citations. Currently uses a keyword retrieval baseline over KB documents
- **Resolver**: Curates a response (response text, citation references, confidence score) grounded in retrieved evidence 
- **Verifier**: Checks security risk, evidence grounding, confidence thresholds. It can override automation since agents propose actions and verifier enforces safety.
- **Decision**: Final operational action: _AUTO_RESOLVE_, _ASK_CLARIFYING_, or _ESCALATE_, based on triage, evidence, and verifier approval


## LangGraph

LangGraph orchestrates the ticket lifecycle as a state machine rather than a linear chain.
This is crucial since support workflows branch based on risk and confidence level, and it may need human approval.

## Planned Upgrades

- LangChain for ticket classification
- RAG-based vector store
- Ticket ingestion using Email APIs, Slack, Zendesk
- Fast API layer along with dashboard

## Project Structure
```
.
├── agents
│   ├── __init__.py
│   ├── agenticClassifier.py
│   ├── agenticDetector.py
│   ├── agenticResolver.py
│   ├── agenticRouter.py
│   ├── agenticVerifier.py
│   └── agentsArchitectureDetails.md
├── apps
│   ├── api.py
│   └── service.py
├── data
│   ├── __init__.py
│   ├── KB
│   │   ├── company_documentation.md
│   │   ├── faqs.md
│   │   └── past_ticket_resolutions.md
│   ├── load_raw_csv.py
│   └── tickets
│       ├── customer_support_tickets.csv
│       └── tickets_private.csv
├── Dockerfile
├── docs
├── graph
│   ├── __init__.py
│   ├── nodes.py
│   ├── state.py
│   └── workflow.py
├── images
│   └── ITSupportSystemsArchitecture.png
├── main.py
├── outputs
│   ├── chroma_db
│   │   └── chroma.sqlite3
│   └── runs
│       ├── ...
├── rag
│   ├── __init__.py
│   ├── chunking.py
│   ├── embeddings.py
│   ├── indexKB.py
│   ├── indexTickets.py
│   ├── loadKB.py
│   ├── prompts.py
│   ├── RAGArchitectureDetails.md
│   ├── retrieve.py
│   ├── utils.py
│   └── vectorDB.py
├── README.md
├── requirements.txt
├── schemas
│   ├── __init__.py
│   ├── decision.py
│   ├── detector.py
│   ├── evidence.py
│   ├── resolution.py
│   ├── SchemasArchitectureDetails.md
│   ├── ticket.py
│   ├── triage.py
│   └── verifier.py
├── scripts
│   ├── eval_run.py
│   ├── metrics.py
│   ├── replay.py
│   └── seedKB.py
└── tests
```

## How To Run

Replay ticket:
```
python scripts/replay.py --n 10
```

Human-In-The-Loop workflow:
```
python main.py
```
## Metrics

Evaluation on a 10-ticket replay run:

- **AUTO_RESOLVE**: 70%
- **ESCALATE**: 30%
- **ASK_CLARIFYING**: 0%
- **Verifier Safe**: 70%
- **Grounded Responses (citations present)**: 100%

These metrics are reflection of the following:
- rule-based classification
- keyword-based KB retrieval
- verifier-based safety gating
- LangGraph orchestration

## References

- Aniket Hingane. “Building an Intelligent Customer Support System with Multi-Agent Architecture.” DEV Community, 28 Dec. 2025, dev.to/exploredataaiml/building-an-intelligent-customer-support-system-with-multi-agent-architecture-236h. 

- https://www.kaggle.com/datasets/suraj520/customer-support-ticket-dataset