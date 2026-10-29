
"""Configuration management for LegalBot.

Supports Google Gemini and Groq.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# Load the project's .env file
load_dotenv(BASE_DIR / ".env", override=True)

# API keys
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()

# Model configuration
default_provider = "google" if GEMINI_API_KEY else "groq"
MODEL_PROVIDER: str = os.getenv(
    "MODEL_PROVIDER", default_provider
).strip().lower()

GEMINI_MODEL: str = os.getenv(
    "GEMINI_MODEL", "gemini-3.6-flash"
).strip()

GROQ_MODEL: str = os.getenv(
    "GROQ_MODEL", "openai/gpt-oss-20b"
).strip()

HOST: str = os.getenv("HOST", "127.0.0.1").strip()
PORT: int = int(os.getenv("PORT", "8000").strip())
REQUEST_TIMEOUT: int = int(
    os.getenv("REQUEST_TIMEOUT", "90").strip()
)

LEGAL_DISCLAIMER: str = (
    "Disclaimer: LegalBot provides educational and informational "
    "guidance based on Indian law. It does not constitute formal "
    "legal advice, representation, or an advocate-client "
    "relationship. Consult a qualified advocate enrolled with "
    "the Bar Council for advice on specific legal matters."
)

DUMMY_API_KEYS = {
    "",
    "your_groq_api_key_here",
    "your_gemini_api_key_here",
    "placeholder",
}


def is_provider_configured() -> bool:
    """Check whether the selected provider has an API key."""
    if MODEL_PROVIDER == "google":
        return bool(
            GEMINI_API_KEY
            and GEMINI_API_KEY not in DUMMY_API_KEYS
        )

    if MODEL_PROVIDER == "groq":
        return bool(
            GROQ_API_KEY
            and GROQ_API_KEY not in DUMMY_API_KEYS
        )

    return False


def is_groq_configured() -> bool:
    """Check whether Groq has an API key configured."""
    return bool(
        GROQ_API_KEY
        and GROQ_API_KEY not in DUMMY_API_KEYS
    )


def get_active_model_name() -> str:
    """Return the active model's display name."""
    if MODEL_PROVIDER == "google":
        return f"Google ({GEMINI_MODEL})"

    if MODEL_PROVIDER == "groq":
        return f"Groq ({GROQ_MODEL})"

    return f"Unknown provider ({MODEL_PROVIDER})"
