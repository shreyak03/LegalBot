"""LegalBot Agents Package."""

from app.agents.legal_team import (
    AGENT_NAMES,
    build_legal_team,
    run_legal_workflow,
)
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_legal_library,
)

__all__ = [
    "AGENT_NAMES",
    "build_legal_team",
    "run_legal_workflow",
    "search_legal_library",
    "get_last_consulted_sources",
    "clear_consulted_sources",
]
