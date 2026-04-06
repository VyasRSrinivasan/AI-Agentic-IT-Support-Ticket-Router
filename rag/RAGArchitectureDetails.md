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
- Defines the embedding interface used by the retrieval backend
- Abstracts model-specific encoding so the rest of the pipeline stays backend-agnostic
- Ensures KB chunks and ticket queries are represented in a shared vector space for similarity search

### Vector Database
(_vectorDB.py_)
- Wraps the vector store implementation used for retrieval
- Provides functions to upsert vectors and query nearest neighbors
- Abstracts storage details to make it easier to swap local vs hosted backends later

### Index Knowledge Base
(_indexKB.py_)
- Builds the searchable KB index from loaded documents
- Converts documents into chunks, computes embeddings, and stores chunk vectors in the vector DB
- Preserves mapping metadata so retrieved chunks can be traced back to original KB sources

### Index Tickets
(_indexTickets.py_)
- Optional support for indexing historical tickets or training examples
- Computes embeddings for ticket text for later similarity or retrieval tasks
- Enables future capabilities like searching prior tickets for similar issues and reusing past resolution context

### Retrieval
(_retrieve.py_)
- Handles query-time retrieval for a given ticket
- Encodes ticket text, searches the vector DB, and returns top matching evidence chunks
- Produces evidence bundles used by the resolver and verifier to ground responses

### Prompts
(_prompts.py_)
- Stores prompt templates and RAG-related prompt design
- Centralizes any LLM prompt text used by retrieval or resolution components
- Helps maintain consistent grounding and evidence usage in generated output
