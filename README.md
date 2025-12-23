---

# RAG + MCP Project (Vector-Based Retrieval System)

## Overview

This project implements a **Retrieval-Augmented system** using **vector embeddings**, a **FAISS vector database**, and **Model Context Protocol (MCP)** tools.

The goal of this project is to demonstrate, end-to-end, how:

* Unstructured documents can be converted into embeddings
* Those embeddings can be stored and searched using semantic similarity
* Retrieval functionality can be exposed as MCP tools
* The system can safely return relevant information **without hallucination**

This implementation focuses on **correctness, clarity, and explainability**, rather than UI or framework-heavy abstractions.

---

## What This Project Is (and Is Not)

### This project **is**:

* A vector-based semantic retrieval system
* A clean example of Retrieval-Augmented design
* An MCP server exposing retrieval tools
* Grounded, deterministic, and explainable

### This project **is not**:

* A chatbot UI
* A keyword-based search engine
* A full LLM-powered conversational agent
* A framework-dependent demo

---

## High-Level Architecture

```
Markdown Documents
        ↓
Semantic Chunking
        ↓
Embeddings Generation
        ↓
FAISS Vector Store
        ↓
Similarity Search
        ↓
Filtering & Confidence Checks
        ↓
MCP Tools (search / answer)
```

---

## Project Structure

```
rag-mcp-project/
│
├── data/
│   └── knowledge_base/
│       └── company_policies.md
│
├── src/
│   ├── ingest.py          # Load and chunk documents
│   ├── embeddings.py     # Generate embeddings
│   ├── vector_store.py   # FAISS vector store
│   ├── build_index.py    # Build & cache vector index
│   ├── retrieval.py      # Retrieval logic
│   └── mcp_server.py     # MCP server & tools
│
├── requirements.txt
├── .env
└── README.md
```

---

## Knowledge Base

The knowledge base consists of **Markdown documents** containing company policies.

Example content:

* Company Leave Policy
* Work From Home Policy
* Security Policy

These documents are **unstructured text**, which makes them unsuitable for traditional relational databases and ideal for vector-based retrieval.

---

## Step-by-Step Implementation Explanation

### 1. Document Ingestion & Chunking (`ingest.py`)

**Purpose**
Convert raw markdown documents into meaningful, retrievable chunks.

**How it works**

* Each markdown file is read
* Content is split by headings (`#`)
* Each section becomes one semantic chunk
* Metadata is attached to each chunk:

  * Section name
  * Source file
  * Chunk ID

**Why this approach**

* One chunk represents one semantic topic
* Prevents unrelated content from mixing
* Keeps retrieval explainable

---

### 2. Embeddings Generation (`embeddings.py`)

**Purpose**
Convert text into numerical representations of meaning.

**How it works**

* Uses a sentence-transformer model
* Each chunk’s text is converted into a high-dimensional vector
* Similar meanings → closer vectors

**Key concept**
Embeddings represent **semantic meaning**, not keywords.

---

### 3. Vector Storage (`vector_store.py`)

**Purpose**
Store embeddings and enable fast similarity search.

**How it works**

* FAISS stores only numeric vectors
* Text and metadata are stored alongside the vectors
* L2 distance is used to compute similarity
* Distance is converted into a similarity score

**Important note**
FAISS always returns the nearest neighbors — even for weak matches.
Relevance is handled at the retrieval layer.

---

### 4. Index Construction (`build_index.py`)

**Purpose**
Build the vector index once and reuse it safely.

**How it works**

* Loads chunks
* Generates embeddings
* Stores embeddings, text, and metadata in FAISS
* Uses lazy initialization (singleton pattern)

**Why this matters**

* Prevents expensive recomputation
* Safe for MCP STDIO mode
* Faster repeated queries

---

### 5. Retrieval Logic (`retrieval.py`)

**Purpose**
Control which results are considered relevant.

**How it works**

* Query is embedded
* FAISS returns top-k nearest vectors
* Results are filtered by:

  * Similarity threshold
  * Deduplication by section
* Returns structured results:

  * Content
  * Metadata
  * Similarity score

**Why thresholds are required**
Vector databases return *nearest*, not *correct*.
Thresholds prevent weak or irrelevant matches from surfacing.

---

### 6. MCP Server & Tools (`mcp_server.py`)

**Purpose**
Expose retrieval functionality via MCP tools.

#### Tool: `search_documents`

* Returns structured evidence
* Includes metadata and similarity scores
* Useful for inspection and debugging

#### Tool: `answer_question`

* Uses retrieved evidence
* Applies an additional confidence gate
* Returns grounded answers only
* Refuses to answer if evidence is weak

**Why MCP**
MCP standardizes how AI capabilities are exposed and consumed by agents or tools.

---

## How Data Flows Through the System

### Example Query

> “What about unused leaves?”

### Flow

```
User Query
   ↓
Query Embedding
   ↓
Vector Similarity Search
   ↓
Top Matching Chunks
   ↓
Threshold & Confidence Checks
   ↓
MCP Tool Response
```

### Important Behavior

* The system retrieves **policy sections**, not sentences
* Fine-grained answers can be layered later using an LLM
* This design avoids hallucination and remains auditable

---

## Testing the System

The system is tested using **MCP Inspector**.

### Start MCP Inspector

```bash
npx @modelcontextprotocol/inspector --stdio
```

### Example Queries

**Search**

```json
{
  "query": "What is the leave policy?",
  "top_k": 3
}
```

**Answer**

```json
{
  "query": "Summarize the security requirements"
}
```

**Negative Case**

```json
{
  "query": "What is the cafeteria menu?"
}
```

Expected behavior:

* Relevant questions return correct policy sections
* Irrelevant questions return:

  > “No relevant information found in the knowledge base.”

---

## Why This Design Is Correct

* Chunking is semantic, not arbitrary
* Retrieval is explainable
* No hallucinated answers
* Confidence-based refusal is supported
* MCP tools are cleanly separated
* Framework-agnostic and extensible

This is a **strong foundation** for adding:

* LLM-based synthesis
* Conversational agents
* UI layers
* Hybrid retrieval (vector + graph)

---

## Key Takeaway

> This project focuses on **retrieval correctness**, not surface-level demos.
> It demonstrates how real-world RAG systems are designed from the inside out.

---

