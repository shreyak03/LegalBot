"""Tools for LegalBot Agno Agents.

Provides access to the sample legal document library with keyword and semantic scoring,
allowing the Legal Research Agent to inspect and cite authentic legal materials.
"""

from typing import List, Set
from app.data.sample_documents import SAMPLE_LEGAL_DOCUMENTS

# Thread-local / query-level source tracking container
_last_consulted_sources: Set[str] = set()


def get_last_consulted_sources() -> List[str]:
    """Retrieve the document titles consulted during the most recent research session."""
    return sorted(list(_last_consulted_sources))


def clear_consulted_sources() -> None:
    """Reset the consulted sources tracker before starting a new inquiry."""
    _last_consulted_sources.clear()


def search_legal_library(query: str) -> str:
    """Search the sample legal knowledge base for relevant statutes, clauses, and guidelines.

    Args:
        query: The search keywords, topic, or legal question to search for.

    Returns:
        A formatted string containing relevant excerpts and citations from the legal library.
    """
    if not query or not query.strip():
        return "No query provided. Please specify legal topics, keywords, or questions."

    query_tokens = [w.lower().strip("?,.;:\"'()") for w in query.split() if len(w) > 2]
    matched_docs = []

    for doc in SAMPLE_LEGAL_DOCUMENTS:
        score = 0
        doc_keywords = [k.lower() for k in doc.get("keywords", [])]
        title_lower = doc.get("title", "").lower()
        content_lower = doc.get("content", "").lower()
        category_lower = doc.get("category", "").lower()

        for token in query_tokens:
            if token in doc_keywords:
                score += 3
            if token in title_lower:
                score += 4
            if token in category_lower:
                score += 2
            if token in content_lower:
                score += 1

        if score > 0:
            matched_docs.append((score, doc))

    if not matched_docs:
        # Return all document titles so the agent knows what exists
        available_titles = ", ".join(f"'{d['title']}'" for d in SAMPLE_LEGAL_DOCUMENTS)
        return (
            f"No direct matches found in legal library for '{query}'. "
            f"Available document categories in library include: {available_titles}."
        )

    # Sort descending by relevance score
    matched_docs.sort(key=lambda item: item[0], reverse=True)

    results: List[str] = []
    for _, doc in matched_docs[:2]:  # Top 2 most relevant documents
        _last_consulted_sources.add(doc["title"])
        # Keep excerpt concise to avoid token exhaustion
        content_preview = doc["content"][:300] + ("..." if len(doc["content"]) > 300 else "")
        results.append(
            f"[{doc['title']}]\nSummary: {doc['summary']}\nKey Rules:\n{content_preview}\n"
        )

    return "\n".join(results)
