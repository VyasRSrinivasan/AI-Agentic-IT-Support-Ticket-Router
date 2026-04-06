# Agents Architecture Details

This document outlines the specialized agents in the ticket routing pipeline. Each agent handles a distinct responsibility, producing structured schemas for modularity, debuggability, and easy replacement. The agents work sequentially to analyze, classify, and decide on ticket handling while ensuring safety and grounding.

## Design Principles

- **Modularity**: Each agent focuses on a single task, using typed inputs and outputs.
- **Safety-First**: Agents like the Detector and Verifier prioritize risk assessment.
- **Grounded Decisions**: Evidence-based reasoning prevents hallucinated responses.
- **Replaceable**: Schema-based interfaces allow swapping implementations (e.g., rule-based to LLM-based).

## Agent Pipeline

### 1. Detector Agent
(_agenticDetector.py_)

- **Purpose**: Performs early safety and completeness checks to identify potential risks or missing information before deeper processing.
- **Key Responsibilities**:
  - Scans ticket content for security risks (e.g., high-risk keywords like "password" or "account breach").
  - Assesses completeness by checking for essential details (e.g., missing contact info or unclear descriptions).
  - Flags issues that could lead to unsafe automation.
- **Input**: `Ticket`
- **Output**: `DetectorOutput` (includes `security_risk` and `missing_info` flags)
- **Example Logic**: Uses keyword matching and heuristic rules for rapid assessment.

### 2. Classifier Agent
(_agenticClassifier.py_)

- **Purpose**: Operationally triages the ticket by categorizing it along multiple dimensions for efficient routing.
- **Key Responsibilities**:
  - Determines the relevant department (e.g., Billing, Technical Support, General).
  - Evaluates urgency (High, Medium, Low) and complexity (Simple, Complex).
  - Assigns a confidence score to reflect classification reliability.
- **Input**: `Ticket`
- **Output**: `TriageOutput` (department, urgency, complexity, confidence)
- **Example Logic**: Rule-based classification based on keywords, product mentions, and ticket metadata.

### 3. Router Agent
(_agenticRouter.py_)

- **Purpose**: Proposes the initial decision on how to handle the ticket, balancing risk, triage, and operational constraints.
- **Key Responsibilities**:
  - Evaluates if auto-resolution is feasible based on detector flags and triage confidence.
  - Suggests escalation for high-risk or complex cases.
  - Recommends clarification if critical information is missing.
- **Input**: `Ticket`, `DetectorOutput`
- **Output**: `Decision` (action type, confidence, routing details)
- **Example Logic**: Threshold-based decision making with safety overrides for security risks.

### 4. Resolver Agent
(_agenticResolver.py_)

- **Purpose**: Generates a proposed automated response, grounded in retrieved evidence from the knowledge base.
- **Key Responsibilities**:
  - Crafts response text using top evidence chunks.
  - Includes citations for transparency and grounding.
  - Provides next steps and a confidence score for the draft.
- **Input**: `Ticket`, `EvidenceBundle`
- **Output**: `ResolutionDraft` (response text, citations, next steps, confidence)
- **Example Logic**: Template-based response generation with evidence integration.

### 5. Verifier Agent
(_agenticVerifier.py_)

- **Purpose**: Acts as the final safety gate, ensuring that proposed automations meet grounding and risk standards before execution.
- **Key Responsibilities**:
  - Validates evidence sufficiency (e.g., minimum citations required).
  - Checks resolution confidence against thresholds.
  - Overrides decisions if safety criteria aren't met (e.g., forces escalation for high-risk tickets).
  - Provides detailed reasons for verification outcomes.
- **Input**: `Ticket`, `Decision`, `ResolutionDraft`, `EvidenceBundle`
- **Output**: `VerificationResult` (safety flag, reasons)
- **Example Logic**: Rule-based checks on confidence, citations, and risk factors.

## Agent Interaction

The agents form a sequential pipeline orchestrated by LangGraph:
1. **Detector** → Identifies risks early.
2. **Classifier** → Triages for routing.
3. **Router** → Proposes action.
4. **Resolver** → Drafts response (if auto-resolving).
5. **Verifier** → Validates and potentially overrides.

This structure ensures decisions are progressive, safe, and evidence-based, minimizing errors in automated ticket handling.