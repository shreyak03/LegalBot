# LegalBot — Multi-Agent Legal Assistant ⚖️

**LegalBot** is an educational, multi-agent legal guidance assistant designed for undergraduate GenAI & ML DevOps coursework. It leverages **FastAPI**, **Agno framework** multi-agent teams, and the **Groq API** (running fast open-weight models such as LLaMA 3.3) with a modern HTML/CSS/JavaScript interface.

---

## 🏛️ Multi-Agent Architecture

LegalBot coordinates exactly **three collaborating agents** via Agno's `Team` framework (`TeamMode.coordinate`):

```
                       +-------------------------+
                       |    User Legal Query     |
                       +------------+------------+
                                    |
                                    v
            +-----------------------------------------------+
            |               Agno Legal Team                 |
            |                                               |
            |  1. Legal Query Analyzer                      |
            |     - Classifies legal domain                 |
            |     - Extracts material facts                 |
            |     - Formulates targeted legal issues        |
            |                        |                      |
            |                        v                      |
            |  2. Legal Research Agent                      |
            |     - Invokes `search_legal_library` tool     |
            |     - Grounded in statutes & contract samples |
            |     - Cites relevant clauses and standards    |
            |                        |                      |
            |                        v                      |
            |  3. Legal Answer Reviewer                     |
            |     - Cross-examines all claims               |
            |     - Strips unsupported / hallucinated points|
            |     - Synthesizes final structured guidance   |
            +-----------------------+-----------------------+
                                    |
                                    v
                     +------------------------------+
                     | Final Reviewed Answer        |
                     | + Consulted Sources          |
                     | + Mandatory Disclaimer       |
                     +------------------------------+
```

1. **Legal Query Analyzer**: Breaks down user inquiries into distinct legal domains (e.g., Tenancy, Intellectual Property, Contract Law, Employment, Consumer Protection) and frames precise research questions.
2. **Legal Research Agent**: Calls the `search_legal_library` tool to investigate sample legal materials, statutes, and contract clauses to ground the findings.
3. **Legal Answer Reviewer**: Audits claims against available evidence, eliminates speculative assertions, ensures prudent legal phrasing, and formats the verified guidance.

---

## 📁 Project Structure

```
LegalBot/
├── .env.example             # Template for environment configuration
├── .gitignore               # Git ignore rules (prevents committing secrets)
├── requirements.txt         # Python project dependencies
├── README.md                # Project documentation and student guide
├── app/
│   ├── __init__.py
│   ├── config.py            # Environment variable loading & secret sanitization
│   ├── main.py              # FastAPI application (GET /, POST /ask, GET /health)
│   ├── schemas.py           # Pydantic models for request & response validation
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── legal_team.py    # Agno Team definition and multi-agent coordination
│   │   └── tools.py         # Legal library search tool for Research Agent
│   ├── data/
│   │   ├── __init__.py
│   │   └── sample_documents.py # Grounding documents (Leases, NDAs, IP, Labor)
│   └── static/
│       ├── index.html       # Clean single-page user interface
│       ├── style.css        # Modern design system & responsive styling
│       └── app.js           # Frontend client logic & progress animation
└── tests/
    ├── __init__.py
    ├── test_health.py       # Tests for /health and / endpoints
    ├── test_validation.py   # Tests for input validation and error handling
    └── test_agents.py       # Tests for Agno agents, Team, and search tool
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10, 3.11, 3.12, 3.13, or 3.14
- A free Groq API key from [Groq Console](https://console.groq.com/keys)

### 2. Setup Virtual Environment

On macOS / Linux:
```bash
# Create a virtual environment
python3 -m venv .venv

# Activate the virtual environment
source .venv/bin/activate

# Install required dependencies
pip install -r requirements.txt
```

On Windows (PowerShell):
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

Open `.env` in any text editor and paste your Groq API key:
```ini
GROQ_API_KEY=gsk_your_actual_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
HOST=127.0.0.1
PORT=8000
REQUEST_TIMEOUT=60
```

---

## 💻 Running the Application

### Option A: Streamlit Frontend (Recommended UI)
Run the clean, white-themed Streamlit web interface:
```bash
streamlit run streamlit_app.py
```
Open your browser at **[http://localhost:8501](http://localhost:8501)**.

### Option B: FastAPI Backend & API Endpoints
Run the FastAPI application:
```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```
- **Web UI & Redirect:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Interactive API Docs (Swagger):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

## 🧪 Running Automated Tests

Run the test suite using `pytest`:
```bash
pytest -v
```

All 12 automated tests verify:
- Health endpoint status and agent registration
- Input validation (empty, whitespace, or short questions)
- Graceful 503 error handling when `GROQ_API_KEY` is not configured
- Agno Team creation, member roles, and tool attachments
- Legal library search accuracy and source tracking

---

## 🔌 API Endpoints

### 1. `GET /`
Serves the responsive single-page web application.

### 2. `GET /health`
Returns system health, active model, and agent registration status without leaking secrets:
```json
{
  "status": "healthy",
  "app_name": "LegalBot — Multi-Agent Legal Assistant",
  "groq_configured": true,
  "model": "llama-3.3-70b-versatile",
  "agents": [
    "Legal Query Analyzer",
    "Legal Research Agent",
    "Legal Answer Reviewer"
  ]
}
```

### 3. `POST /ask`
Submits a query to the multi-agent team.

**Request Body:**
```json
{
  "question": "Can a landlord deduct cleaning charges from a tenant's security deposit without providing an itemized statement?"
}
```

**Response Body:**
```json
{
  "status": "success",
  "question": "Can a landlord deduct cleaning charges from a tenant's security deposit without providing an itemized statement?",
  "answer": "### Legal Classification & Summary...",
  "sources": [
    "Residential Lease & Security Deposits Statutory Guidelines"
  ],
  "disclaimer": "Disclaimer: LegalBot provides educational and informational guidance only..."
}
```

---

## 🎓 Note for Students: Assignment Scope

This starter project contains the functional application layer. **As part of your GenAI + ML DevOps assignment, you will independently implement:**
1. **Containerization:** Create an optimized `Dockerfile` for the FastAPI service.
2. **Local Multi-Container Orchestration:** Build a `docker-compose.yml` (or `compose.yaml`) with volume mounts, environment isolation, and healthchecks.
3. **Cloud-Native Deployment:** Author Kubernetes manifests (Deployments, Services, ConfigMaps, Secrets, Ingress, and Resource Limits) or Helm charts.
4. **CI/CD Pipeline:** Configure automated testing and container image building workflows.

---

## ⚖️ Legal Disclaimer

*LegalBot is built exclusively for educational and demonstrative purposes. It provides generalized informational summaries and does not constitute legal advice, representation, or an attorney-client relationship. Always consult a qualified, licensed attorney for legal counsel.*
