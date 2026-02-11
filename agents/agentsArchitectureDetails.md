# Agents Architecture Details

Each agent in the pipeline represents a particular responsibility where agents produce schemas to ensure it is replaceable and debuggable.

## Pipeline

### 1. Detector Agent 
(_agenticDetector.py_)

- **Purpose:** Early safety/compliance check before further processing
- **Input:** `Ticket`
- **Output:** `DetectorOutput`

### 2. Classifier Agent
(_agenticClassifier.py_)

- **Purpose:** Triage the ticket operationally
- **Input:** `Ticket`
- **Output:** `TriageOutput`

### 3. Router Agent
(_agenticRouter.py_)

- **Purpose:** Propose the next step with risk & triage in mind.
- **Input:** `Ticket`, `DetectorOutput`
- **Output:** `Decision`

### 4. Resolver Agent
(_agenticResolver.py_)

- **Purpose:** Draft a grounded response by utilizing the retrieved evidence.
- **Input:** `Ticket`, `EvidenceBundle`
- **Output:** `ResolutionDraft`

### 5. Verifier Agent
(_agenticVerifier.py_)

- **Purpose:** Enforce safety before allowing automation
- **Input:** `Ticket`, `Decision`, `ResolutionDraft`, `EvidenceBundle`
- **Output:** `VerificationResult`