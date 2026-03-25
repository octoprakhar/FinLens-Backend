# 📄 **FinLens V0 — Project Scope Document**

## **1. Objective**

The objective of **FinLens V0** is to build a minimal, functional system that can:

> Ingest long-form financial PDF documents (e.g., 200+ page annual reports), convert them into structured textual representations, and enable users to query the document using natural language while receiving answers supported by verifiable source citations (page-level).

---

## **2. Scope Definition**

### **2.1 In-Scope Functionalities**

The system will include the following core components:

---

### **A. Document Ingestion & Parsing**

* Accept a PDF document as input (e.g., annual report of a company such as Tata Motors).
* Extract text content from each page of the PDF.
* Preserve page-level boundaries during extraction.
* Convert extracted content into a structured **Markdown format**.
* Store page numbers alongside corresponding text.

**Output Requirement:**

* A `.md` file (or equivalent structured format) where:

  * Each section is associated with a page number.
  * Content is readable and segmented by pages.

---

### **B. Text Chunking**

* Split the parsed Markdown into smaller, semantically meaningful chunks.
* Each chunk must include:

  * Text content
  * Page number (mandatory)
  * Optional section/header metadata (if available)

**Objective:**

* Ensure chunks are suitable for embedding and retrieval.

---

### **C. Embedding & Storage**

* Convert each text chunk into vector embeddings using a suitable embedding model.
* Store embeddings along with metadata:

  * Chunk text
  * Page number
* Use a simple storage mechanism for V0:

  * Local in-memory structure, file-based storage, or FAISS index

---

### **D. Retrieval Mechanism**

* Accept a natural language query from the user.
* Retrieve top-k most relevant chunks using similarity search (e.g., cosine similarity).
* Ensure retrieved results maintain traceability to original page numbers.

---

### **E. Question Answering with Citations**

* Pass the user query along with retrieved chunks to a language model.
* Generate a natural language answer based only on retrieved content.
* Include **explicit page-level citations** in the response.

**Output Requirement:**

* Answer must:

  * Be grounded in retrieved text
  * Include page references (e.g., “Page 134”)

---

## **3. Out of Scope (Explicitly Excluded in V0)**

The following features are intentionally excluded from V0:

* ❌ KPI dashboard or financial metric extraction
* ❌ Multi-agent systems (e.g., Auditor/Strategist roles)
* ❌ Audio summaries or speech generation
* ❌ Multi-document or comparative analysis
* ❌ Advanced table reconstruction or financial modeling
* ❌ Authentication, user accounts, or production deployment
* ❌ Full UI/UX polish (basic interface acceptable if implemented)

---

## **4. Non-Functional Requirements**

* The system should handle large PDFs (≥ 100 pages) without crashing.
* Processing should be modular (separate ingestion, chunking, retrieval).
* Code should be structured and maintainable (not notebook-only).
* Outputs must be **traceable and debuggable** (especially page references).
* Accuracy is prioritized over speed for V0.

---

## **5. Success Criteria**

FinLens V0 will be considered successful if:

1. A large annual report PDF can be ingested and converted into structured text.
2. The system can answer user queries based on the document.
3. Every answer includes correct and verifiable page-level citations.
4. Retrieval returns contextually relevant chunks for most queries.
5. The pipeline works end-to-end without manual intervention.

---

## **6. Suggested Technical Stack (Flexible)**

* **PDF Parsing:** PyMuPDF (`fitz`), pdfplumber, or Docling (optional upgrade)
* **Text Processing:** Python
* **Embeddings:** OpenAI / Gemini / Sentence Transformers
* **Vector Storage:** FAISS (preferred for V0) or simple in-memory
* **Backend (optional later):** FastAPI
* **Frontend (optional later):** Next.js

---

## **7. Development Phases (Execution Order)**

1. PDF → Markdown extraction
2. Chunking with metadata
3. Embedding + storage
4. Retrieval system
5. Question answering with citation

---

## **8. Key Design Principle**

> Prioritize correctness, traceability, and simplicity over feature richness.

---

## **9. Future Extensions (Post V0)**

(To be considered only after V0 completion)

* KPI extraction dashboard
* Comparative financial analysis
* Table-aware querying
* Multi-agent verification
* Audio summaries

---


# 📄 **FinLens V1 — Project Scope Document**

---

## **1. Objective**

The objective of **FinLens V1** is to evolve the V0 system into a **responsive, scalable, and user-friendly API-driven application** by introducing asynchronous processing, state management, and system efficiency improvements.

> FinLens V1 focuses on improving system usability, responsiveness, and lifecycle management while preserving the core document understanding capabilities established in V0.

---

## **2. Scope Definition**

### **2.1 In-Scope Functionalities**

The system will extend V0 capabilities with the following components:

---

### **A. Asynchronous Document Processing**

* Decouple document upload from processing pipeline.
* Upon upload, immediately return a unique `file_id` and initial processing status.
* Execute ingestion, chunking, and embedding pipeline in the background.

**Objective:**

* Improve API responsiveness and user experience.
* Avoid blocking requests for large documents.

**Output Requirement:**

* Upload API returns:

  * `file_id`
  * `status = "processing"`

---

### **B. Document Status Tracking**

* Maintain processing state for each uploaded document.

* Supported states:

  * `processing`
  * `ready`
  * `failed`
  * `not_found`

* Provide a dedicated API to check document status.

**Objective:**

* Enable clients to track processing lifecycle.
* Ensure safe querying only when data is ready.

---

### **C. Conditional Query Execution**

* Modify query endpoint to validate document readiness.
* Prevent query execution if document is still processing or failed.

**Output Requirement:**

* If not ready:

  * Return appropriate status message.
* If ready:

  * Proceed with retrieval + QA pipeline.

---

### **D. Response Caching with Expiry**

* Cache query responses based on `(file_id, query)` pair.
* Introduce TTL (Time-To-Live) for cache invalidation.

**Objective:**

* Reduce redundant LLM calls.
* Improve response latency.

---

### **E. Retrieval Debugging Interface**

* Provide an endpoint to retrieve top-k relevant chunks without invoking the LLM.
* Include:

  * chunk text
  * page number
  * similarity score

**Objective:**

* Enable debugging and evaluation of retrieval quality.
* Reduce dependency on LLM during development.

---

### **F. Data Lifecycle Management (Cleanup)**

* Provide endpoint to delete all data associated with a `file_id`.
* Remove:

  * uploaded files
  * processed markdown
  * chunk files
  * embeddings / FAISS index
  * cached responses

**Objective:**

* Manage disk usage.
* Support multi-user scalability.

---

### **G. Improved API Design (Service Layer Separation)**

* Separate business logic from route handlers.
* Introduce service layer modules for:

  * ingestion
  * processing
  * retrieval / QA

**Objective:**

* Improve code maintainability and scalability.

---

## **3. Out of Scope (Explicitly Excluded in V1)**

The following features remain excluded:

* ❌ Migration to distributed vector databases (e.g., Pinecone, Weaviate)
* ❌ Cloud storage integration (e.g., Amazon S3)
* ❌ Authentication and multi-user account management
* ❌ Advanced table reconstruction
* ❌ Multi-document querying
* ❌ Conversational memory (multi-turn context)
* ❌ Frontend UI/UX enhancements beyond basic usage

---

## **4. Non-Functional Requirements**

* Upload API must respond immediately (non-blocking behavior).
* System must support concurrent document processing.
* Query latency should improve via caching.
* System must handle multiple document sessions independently.
* Data must be isolated per `file_id`.
* System should remain debuggable and traceable.

---

## **5. Success Criteria**

FinLens V1 will be considered successful if:

1. Upload API returns instantly without waiting for processing.
2. Document processing occurs asynchronously and reliably.
3. Status endpoint correctly reflects processing state.
4. Queries are only executed on fully processed documents.
5. Cached responses reduce repeated LLM calls.
6. Retrieval debugging endpoint returns meaningful chunks.
7. Cleanup endpoint successfully removes all related data.
8. System supports multiple documents without conflict.

---

## **6. Suggested Technical Stack (V1 Additions)**

* **Backend Framework:** FastAPI
* **Background Tasks:** FastAPI BackgroundTasks (V0-level async)
* **Caching:** In-memory dictionary (upgrade later to Redis)
* **Vector Storage:** FAISS (continue from V0)
* **Task Orchestration (Future):** Celery

---

## **7. Development Phases (Execution Order)**

1. Introduce background processing for upload pipeline
2. Implement document status tracking
3. Update query endpoint with status validation
4. Add response caching with TTL
5. Build retrieval-only debugging endpoint
6. Implement cleanup endpoint
7. Refactor code into service-layer architecture

---

## **8. Key Design Principle**

> Prioritize responsiveness, system reliability, and lifecycle management over adding new ML capabilities.

---

## **9. Future Extensions (Post V1)**

* Migration to scalable vector databases (e.g., Qdrant)
* Cloud storage integration
* Multi-document querying
* Table-aware understanding
* Conversational memory
* User authentication & dashboards

---
