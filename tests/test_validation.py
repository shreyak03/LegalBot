
"""Tests for Input Validation and Error Handling."""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_ask_empty_payload():
    """Verify empty POST payload returns 422 Unprocessable Entity."""
    response = client.post("/ask", json={})

    assert response.status_code == 422


def test_ask_short_question():
    """Verify questions shorter than five characters are rejected."""
    response = client.post("/ask", json={"question": "law?"})

    assert response.status_code == 422


def test_ask_whitespace_only():
    """Verify whitespace-only questions are rejected."""
    response = client.post("/ask", json={"question": "          "})

    assert response.status_code == 422


def test_ask_missing_api_key(monkeypatch):
    """Verify 503 when the active provider has no API key."""
    monkeypatch.setattr("app.config.MODEL_PROVIDER", "groq")
    monkeypatch.setattr("app.config.GROQ_API_KEY", "")
    monkeypatch.setattr("app.config.GEMINI_API_KEY", "")

    response = client.post(
        "/ask",
        json={
            "question": (
                "Can a landlord keep my deposit without a receipt?"
            )
        },
    )

    assert response.status_code == 503

    data = response.json()
    assert "Groq API key is not configured" in data["detail"]


def test_ask_success_with_mocked_workflow(monkeypatch):
    """Verify a successful response with a mocked agent workflow."""
    monkeypatch.setattr("app.config.MODEL_PROVIDER", "groq")
    monkeypatch.setattr(
        "app.config.GROQ_API_KEY",
        "mock_valid_key_123",
    )

    mock_result = {
        "answer": (
            "The rules governing security deposits depend on "
            "applicable state law and the tenancy agreement."
        ),
        "sources": [
            "Model Tenancy Act and applicable state rent laws"
        ],
    }

    with patch(
        "app.main.run_legal_workflow",
        return_value=mock_result,
    ):
        response = client.post(
            "/ask",
            json={
                "question": (
                    "Can a landlord withhold my deposit "
                    "without itemized deductions?"
                )
            },
        )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "success"
    assert "security deposits" in data["answer"]
    assert (
        "Model Tenancy Act and applicable state rent laws"
        in data["sources"]
    )
    assert "Disclaimer:" in data["disclaimer"]
