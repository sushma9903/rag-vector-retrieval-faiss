# src/retrieval.py

from embeddings import embed_texts

SIMILARITY_THRESHOLD = 0.45  # tuneable, conservative default


def retrieve(query, store, top_k=3):
    """
    Retrieve top-k relevant chunks for a query with filtering and deduplication.
    Returns structured results.
    """
    query_embedding = embed_texts([query])[0]

    # Vector store returns list of (content, metadata, score)
    results = store.search(query_embedding, top_k)

    filtered = []
    seen_sections = set()

    for item in results:
        content = item["content"]
        metadata = item["metadata"]
        score = item["score"]

        # Drop weak matches
        if score < SIMILARITY_THRESHOLD:
            continue

        # Deduplicate by section
        section = metadata.get("section")
        if section in seen_sections:
            continue

        seen_sections.add(section)

        filtered.append({
            "content": content,
            "metadata": metadata,
            "score": score
        })

    return filtered
