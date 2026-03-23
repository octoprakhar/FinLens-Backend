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
