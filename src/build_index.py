# src/build_index.py

from ingest import load_and_chunk_documents
from embeddings import embed_texts
from vector_store import VectorStore

_store = None  # private singleton


def get_vector_store():
    """
    Lazily build and return the vector store.
    Safe for MCP STDIO mode.
    """
    global _store

    if _store is None:
        chunks = load_and_chunk_documents()

        texts = [chunk["content"] for chunk in chunks]
        metadatas = [chunk["metadata"] for chunk in chunks]

        embeddings = embed_texts(texts)

        store = VectorStore(dim=len(embeddings[0]))
        store.add(embeddings, texts, metadatas)

        _store = store

    return _store
