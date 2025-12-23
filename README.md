---

# 📄 Foundational RAG (Retrieval-Augmented Generation) – Retrieval Layer Implementation

## Overview

This project implements the **foundational retrieval layer of a Retrieval-Augmented Generation (RAG) system**.
The focus of this implementation is on **document processing, embedding generation, vector storage, and similarity-based retrieval**.

The project intentionally **does not include LLM-based answer generation**, as the goal is to clearly understand and demonstrate how the **retrieval component of RAG works in isolation**.

---

## What This Project Demonstrates

This repository covers the following core RAG concepts:

* Creating a document-based knowledge base using Markdown files
* Splitting documents into smaller, meaningful chunks
* Generating vector embeddings for each chunk
* Storing embeddings in a FAISS vector database
* Performing similarity search to retrieve the most relevant chunks for a user query
* Returning retrieved content along with metadata and similarity scores

---

## High-Level Architecture

The overall flow of the system is as follows:

1. **Document Loading**
   Markdown documents are loaded from the knowledge base directory.

2. **Chunking**
   Documents are split into overlapping text chunks to preserve context.

3. **Embedding Generation**
   Each chunk is converted into a vector embedding using a sentence-level embedding model.

4. **Vector Storage**
   Embeddings are stored in a FAISS vector index for efficient similarity search.

5. **Query Retrieval**
   A user query is embedded and compared against stored vectors to retrieve the most relevant chunks.

---

## Project Structure

```
rag-project/
│
├── data/
│   └── knowledge_base/
│       └── *.md                # Source documents
│
├── src/
│   ├── load_and_chunk.py       # Document loading and chunking logic
│   ├── embeddings.py           # Embedding generation
│   ├── vector_store.py         # FAISS index creation and storage
│   ├── retrieve.py             # Similarity search and retrieval
│
├── main.py                     # Entry point to run retrieval
├── requirements.txt            # Project dependencies
└── README.md                   # Project documentation
```

---

## Tech Stack

* **Python**
* **SentenceTransformers** – for text embeddings
* **FAISS** – for vector storage and similarity search

---

## How to Run the Project

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Add Documents

Place your Markdown documents inside:

```
data/knowledge_base/
```

### 3. Run the Retrieval Pipeline

```bash
python main.py
```

---

## Example Usage

**Sample Query:**

```
What is the company leave policy?
```

**Sample Output:**

* Retrieved text chunk related to leave policy
* Metadata (document name, section, chunk ID)
* Similarity score indicating relevance

This output can later be passed to an LLM for answer generation, if required.

---

## Scope Clarification

This project focuses **only on the retrieval layer** of a RAG system.

The following are **intentionally excluded**:

* LLM-based answer generation
* Chat interfaces or UI
* Agent frameworks or orchestration logic

These can be added as extensions in future tasks.

---

## Learning Outcome

By completing this project, you gain a clear understanding of:

* Why chunking is required in RAG systems
* How embeddings represent text semantically
* How vector databases enable efficient retrieval
* How retrieval augments language models with external knowledge

---

## Future Enhancements (Optional)

* Integrate an LLM to generate answers using retrieved context
* Add hybrid retrieval (keyword + vector search)
* Expose retrieval as an API or tool
* Implement confidence-based filtering for responses

---

## Author

**Sushma S**
AI Intern – BlazeUp Training Program

---
