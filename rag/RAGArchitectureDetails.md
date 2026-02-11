# RAG Architecture Details


### Load Knowledge Base
(_loadKB.py_)
- Loads KB documents from `data/KB/`
- Outputs `(doc_id, text)` pairs
- Keeps the KB format flexible


### Chunking
(_chunking.py_)
- Splits long KB docs into smaller chunks
- Utilizes chunk size and overlap to enhance retrieval precision
- Stops documents with large amounts of context from harming search quality

### Utilities
(_utils.py_)
- Text cleanup & normalization
- Hashing for chunk IDs
- Metadata helpers to ensure that each chunk has consistent fields

### Embeddings
(_embeddings.py_)
- Defines embedding interface that's used by retrieval backend

### Vector Database
(_vectorDB.py_)

### Index Knowledge Base
(_indexKB.py_)

### Index Tickets
(_indexTickets.py_)

### Retrieval 
(_retrieve.py_)

### Prompts
(_prompts.py_)