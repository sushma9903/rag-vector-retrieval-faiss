from sentence_transformers import SentenceTransformer

# Load the model once when the module is imported
_model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_texts(texts):
    """
    Generate embeddings locally using sentence-transformers.
    Input: list of strings
    Output: list of vectors (list of floats)
    """
    return _model.encode(texts, convert_to_numpy=True).tolist()
