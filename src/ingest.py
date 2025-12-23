from pathlib import Path

def load_and_chunk_documents():
    """
    Load markdown documents and chunk them by section headings.
    Returns a list of structured chunks with metadata.
    """
    docs_path = Path("data/knowledge_base")
    chunks = []

    for file in docs_path.glob("*.md"):
        content = file.read_text(encoding="utf-8")
        sections = _split_markdown_by_heading(content)

        for idx, section in enumerate(sections):
            chunks.append({
                "content": section["content"].strip(),
                "metadata": {
                    "section": section["title"],
                    "source": file.name,
                    "chunk_id": idx
                }
            })

    return chunks


def _split_markdown_by_heading(text):
    """
    Split markdown text into sections based on headings.
    """
    sections = []
    current_title = None
    current_content = []

    for line in text.splitlines():
        if line.startswith("#"):
            if current_title:
                sections.append({
                    "title": current_title,
                    "content": "\n".join(current_content)
                })
            current_title = line.lstrip("#").strip()
            current_content = []
        else:
            current_content.append(line)

    if current_title:
        sections.append({
            "title": current_title,
            "content": "\n".join(current_content)
        })

    return sections
