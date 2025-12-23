from dotenv import load_dotenv
load_dotenv()

from mcp.server.fastmcp import FastMCP
from build_index import get_vector_store
from retrieval import retrieve

mcp = FastMCP("RAG MCP Server")


@mcp.tool()
def search_documents(query: str, top_k: int = 3) -> list:
    """
    Retrieve relevant policy sections as evidence.
    Returns structured chunks with metadata and similarity scores.
    """
    store = get_vector_store()
    return retrieve(query, store, top_k)


@mcp.tool()
def answer_question(query: str) -> str:
    """
    Answer a question using retrieved context from the knowledge base.
    This is a true RAG-style answer (retrieval + synthesis).
    """
    store = get_vector_store()
    results = retrieve(query, store, top_k=3)

    # SECOND-GATE CHECK (critical)
    if not results or results[0]["score"] < 0.55:
        return "No relevant information found in the knowledge base."

    context = "\n\n".join(
        f"{item['metadata']['section']}:\n{item['content']}"
        for item in results
    )

    return context



if __name__ == "__main__":
    mcp.run(transport="stdio")
