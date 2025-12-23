# src/vector_store.py

import faiss
import numpy as np


class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.metadatas = []

    def add(self, embeddings, texts, metadatas):
        """
        Add embeddings with associated texts and metadata to the vector store.
        """
        vectors = np.array(embeddings).astype("float32")
        self.index.add(vectors)

        self.texts.extend(texts)
        self.metadatas.extend(metadatas)

    def search(self, query_embedding, top_k=3):
        """
        Search for similar vectors and return structured results.
        """
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []

        for idx, dist in zip(indices[0], distances[0]):
            if idx == -1:
                continue

            results.append({
                "content": self.texts[idx],
                "metadata": self.metadatas[idx],
                "score": float(1 / (1 + dist))  # similarity score
            })

        return results
