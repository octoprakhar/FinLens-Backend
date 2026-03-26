# 📄 **FinLens — AI-Powered Financial Document Intelligence**

## 🔹 Overview

**FinLens** is an end-to-end system that transforms complex financial documents (e.g., 200+ page annual reports) into a **queryable knowledge system** powered by modern **Retrieval-Augmented Generation (RAG)**.

> Users can upload financial PDFs and ask natural language questions, receiving **accurate answers with verifiable page-level citations**.

---

## 🔹 Key Highlights

* 📄 Handles **large PDFs (100–600+ pages)**
* 🔍 **Semantic search** over document content
* 🧠 **LLM-powered answers with citations**
* ⚡ **Asynchronous processing** for responsiveness
* 🗂️ **Session-based document isolation**
* 🚀 Built with **production-oriented architecture**

---

## 🧱 System Architecture

```
Upload → Ingestion → Chunking → Embedding → FAISS Index
       → Retrieval → LLM (RAG) → Answer + Citations
```

---

# 📦 **FinLens V0 — Core Intelligence Layer**

## 🎯 Objective

Build a minimal system that:

* Converts PDFs → structured text
* Enables semantic search
* Generates answers grounded in document context

---

## ⚙️ Core Components

### A. Document Ingestion

* PDF parsing using PyMuPDF (`fitz`)
* Page-level text extraction
* Structured Markdown generation

### B. Chunking

* Paragraph-based segmentation
* Sentence-aware chunk creation
* Page metadata preserved

### C. Embedding & Storage

* Sentence Transformers (`all-MiniLM-L6-v2`)
* FAISS vector index for similarity search

### D. Retrieval

* Top-k semantic chunk retrieval
* Cosine similarity-based search

### E. Question Answering (RAG)

* Context-grounded LLM responses
* Explicit **page-level citations**

---

## ✅ Outcome

* End-to-end working RAG pipeline
* Accurate retrieval + grounded answers
* Fully traceable outputs

---

# ⚡ **FinLens V1 — System & API Layer**

## 🎯 Objective

Transform V0 into a **scalable backend system** with:

* Async processing
* API architecture
* Performance optimizations

---

## 🚀 New Capabilities

### A. Asynchronous Processing

* Background pipeline execution using FastAPI
* Instant upload response with `file_id`

---

### B. Document Lifecycle Management

* Status tracking:

  * `processing`, `ready`, `failed`
* Safe query gating

---

### C. Intelligent Caching

* TTL-based caching for `(file_id, query)`
* Reduces LLM cost & latency

---

### D. Retrieval Debugging Endpoint

* Inspect top-k chunks without LLM
* Includes:

  * text
  * page
  * similarity score

---

### E. Cleanup & Resource Management

* Delete all session data:

  * uploads
  * chunks
  * embeddings
  * FAISS index
  * cache

---

### F. Modular Backend Architecture

```
routes → services → components → artifacts/config
```

* Clean separation of concerns
* Scalable and maintainable design

---

## ✅ Outcome

* Fully functional **API-driven RAG system**
* Handles **multiple documents concurrently**
* Improved performance and debuggability

---

# 🧠 **FinLens V2 — (Planned Enhancements)**

## 🎯 Objective

Enhance **data understanding, scalability, and production readiness**

---

## 🔍 A. Table Understanding (HIGH IMPACT)

### Problem

* Financial PDFs heavily rely on tables
* Current system treats tables as broken text

### Solution Direction

* Integrate table-aware parsing:

  * `pdfplumber` OR
  * advanced parsers like Docling
* Represent tables as:

  * structured JSON
  * or Markdown tables

### Future Capability

* Queries like:

  > “What is total revenue in 2023?”

---

## ⚡ B. Scalable Vector Storage

* Replace FAISS with:

  * **Qdrant**
  * **Pinecone**
  * **Weaviate**

---

## ☁️ C. Cloud Storage

* Store PDFs in:

  * AWS S3 / GCP Storage
* Avoid local disk limitations

---

## 🚀 D. Distributed Processing

* Move from FastAPI BackgroundTasks → **Celery + Redis**
* True async job queue

---

## 💬 E. Conversational Memory

* Multi-turn Q&A over documents
* Context-aware responses

---

## 📊 F. Evaluation Framework

* Automated testing of:

  * retrieval quality
  * answer correctness
* Build benchmark dataset

---

## 🔐 G. Authentication & Multi-User Support

* User sessions
* Document ownership
* API security

---

# 🛠️ Tech Stack

### Backend

* FastAPI

### ML / NLP

* Sentence Transformers
* FAISS
* Google Gemini

### PDF Processing

* PyMuPDF

---

# 🧩 Key Design Principles

> ✔ Simplicity over premature complexity
> ✔ Traceability (page-level citations)
> ✔ Modular architecture
> ✔ Production-oriented thinking

