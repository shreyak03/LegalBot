
"""Tests for Health and Frontend Endpoints."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_endpoint():
    """Verify /health returns 200 and reports the three agents."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"
    assert "LegalBot" in data["app_name"]
    assert isinstance(data["model"], str)
    assert data["model"]
    assert isinstance(data["groq_configured"], bool)

    agents = data["agents"]

    assert isinstance(agents, list)
    assert len(agents) == 3

    expected_agents = {
        "Legal Query Analyzer",
        "Legal Research Agent",
        "Legal Answer Reviewer",
    }

    assert expected_agents.issubset(set(agents))


def test_root_serves_frontend():
    """Verify GET / returns the LegalBot HTML frontend."""
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "LegalBot" in response.text


def test_frontend_contains_agent_names():
    """Verify the frontend displays the expected agent names."""
    response = client.get("/")

    assert response.status_code == 200

    expected_agents = [
        "Legal Query Analyzer",
        "Legal Research Agent",
        "Legal Answer Reviewer",
    ]

    for agent in expected_agents:
        assert agent in response.text, (
            f"Expected agent name not found in frontend: {agent}"
        )
