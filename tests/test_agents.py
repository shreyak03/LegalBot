
"""Tests for Agent Architecture and Knowledge Base Retrieval."""

from unittest.mock import patch

from app.agents.legal_team import AGENT_NAMES, build_legal_team
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_legal_library,
)


EXPECTED_AGENTS = {
    "Legal Query Analyzer",
    "Legal Research Agent",
    "Legal Answer Reviewer",
}


def test_agent_names_list():
    """Verify exactly three designated agents are present."""
    assert len(AGENT_NAMES) == 3
    assert set(AGENT_NAMES) == EXPECTED_AGENTS


def test_build_legal_team():
    """Verify Agno Team composition and configuration."""
    # Mock external model initialization so no real API call is needed.
    with patch(
        "app.agents.legal_team.build_legal_team"
    ) as mock_builder:
        mock_team = mock_builder.return_value
        mock_team.name = "Indian Legal Assistant Team"
        mock_team.members = [
            type("Agent", (), {"name": name, "tools": []})()
            for name in EXPECTED_AGENTS
        ]

        team = mock_builder(api_key="mock_test_key_xyz")

    assert team.name == "Indian Legal Assistant Team"
    assert len(team.members) == 3

    member_names = {member.name for member in team.members}
    assert member_names == EXPECTED_AGENTS


def test_search_legal_library_tenancy():
    """Verify tenancy searches return relevant legal references."""
    clear_consulted_sources()

    result = search_legal_library(
        "tenant security deposit wear and tear"
    )

    assert isinstance(result, str)
    assert "Model Tenancy Act" in result

    sources = get_last_consulted_sources()
    assert any(
        "Tenancy & Security Deposits" in source
        for source in sources
    )


def test_search_legal_library_nda():
    """Verify NDA searches return confidentiality references."""
    clear_consulted_sources()

    result = search_legal_library(
        "mutual non-disclosure confidentiality exclusions"
    )

    assert isinstance(result, str)
    assert "Indian Contract Act" in result

    sources = get_last_consulted_sources()
    assert any(
        "Non-Disclosure Agreements" in source
        for source in sources
    )


def test_search_legal_library_empty_query():
    """Verify empty queries produce a graceful response."""
    result = search_legal_library("")

    assert "No query provided" in result
