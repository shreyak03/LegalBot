# LegalBot — Docker Containerization Lab Manual 🐳

**Lab Assignment:** GenAI & ML DevOps Lab — Containerization  
**Project:** LegalBot (Multi-Agent Legal Assistant)  
**Supported OS:** Windows (PowerShell / CMD), macOS (Apple Silicon / Intel), Linux (Ubuntu / Debian)

---

## 1. Prerequisites & Verification

Ensure Docker is installed and running on your system:
- **Windows:** Install [Docker Desktop for Windows](https://www.docker.com/products/docker-desktop/) (enable WSL 2).
- **macOS:** Install Docker Desktop for Mac (Apple Silicon or Intel).
- **Linux:** Install Docker Engine (`sudo apt-get install -y docker.io`).

**Verify Installation (in your terminal):**
```bash
docker --version
docker compose version
```

---

## 2. Step 1: Create `.dockerignore`

Create a file named `.dockerignore` in the project root (`LegalBot/`) to exclude virtual environments, cache, and local secrets from image layers.

```text
# Virtual environments & caches
.venv/
venv/
env/
__pycache__/
*.py[cod]
.pytest_cache/

# Git and editor metadata
.git/
.gitignore
.vscode/
.idea/

# Environment files & docs
.env
*.md
DOCKER_LAB_GUIDE.*
.DS_Store
Thumbs.db
```

---

## 3. Step 2: Create `Dockerfile`

Create a file named `Dockerfile` (no extension) in the project root (`LegalBot/`):

```dockerfile
# 1. Minimal Python base image
FROM python:3.11-slim

# 2. Optimize Python runtime environment
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

# 3. Install curl for container healthcheck
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# 4. Copy & install dependencies first (layer caching)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# 5. Copy application source code
COPY app/ /app/app/
COPY streamlit_app.py /app/streamlit_app.py

# 6. Expose FastAPI (8000) and Streamlit (8501) ports
EXPOSE 8000 8501

# 7. Health check endpoint
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://127.0.0.1:8000/health || exit 1

# 8. Default command: Start FastAPI server
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 4. Step 3: Build the Docker Image

Run from the `LegalBot/` root directory where your `Dockerfile` is located.

* **Windows (PowerShell / CMD):**
  ```powershell
  docker build -t legalbot:latest .
  ```
* **macOS & Linux (Terminal):**
  ```bash
  docker build -t legalbot:latest .
  ```
  *(Note for Apple Silicon M1/M2/M3/M4 if cross-compiling for x86: add `--platform linux/amd64`)*

**Verify Image Creation:**
```bash
docker images legalbot
```

---

## 5. Step 4: Run the Container

Pass your API keys dynamically using `--env-file .env` (never hardcode keys inside the Dockerfile).

### Mode A: FastAPI Backend & Web UI (Port 8000 — Default)

* **Windows (PowerShell):**
  ```powershell
  docker run -d --name legalbot-app -p 8000:8000 --env-file .env legalbot:latest
  ```
* **Windows (CMD):**
  ```cmd
  docker run -d --name legalbot-app -p 8000:8000 --env-file .env legalbot:latest
  ```
* **macOS & Linux:**
  ```bash
  docker run -d --name legalbot-app -p 8000:8000 --env-file .env legalbot:latest
  ```

---

### Mode B: Streamlit Dashboard (Port 8501 — Alternative)

* **Windows (PowerShell / CMD):**
  ```powershell
  docker run -d --name legalbot-streamlit -p 8501:8501 --env-file .env legalbot:latest streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
  ```
* **macOS & Linux:**
  ```bash
  docker run -d --name legalbot-streamlit -p 8501:8501 --env-file .env legalbot:latest streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0
  ```

---

## 6. Step 5: Verify & Test

1. **Check Container Status:**
   ```bash
   docker ps
   ```
2. **View Live Application Logs:**
   ```bash
   docker logs -f legalbot-app
   ```
   *(Press `Ctrl + C` to exit logs)*

3. **Access in Browser:**
   - **FastAPI Web UI:** [http://localhost:8000](http://localhost:8000)
   - **FastAPI Swagger Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
   - **FastAPI Health Check:** [http://localhost:8000/health](http://localhost:8000/health)
   - **Streamlit UI (if using Mode B):** [http://localhost:8501](http://localhost:8501)

4. **Health Check via Terminal:**
   * **Windows (PowerShell):**
     ```powershell
     Invoke-RestMethod -Uri http://localhost:8000/health | ConvertTo-Json
     ```
   * **macOS / Linux:**
     ```bash
     curl http://localhost:8000/health
     ```

---

## 7. Container Lifecycle Commands

| Action | Command |
| :--- | :--- |
| **List running containers** | `docker ps` |
| **List all containers (including stopped)** | `docker ps -a` |
| **View logs** | `docker logs legalbot-app` |
| **Stream live logs** | `docker logs -f legalbot-app` |
| **Stop container** | `docker stop legalbot-app` |
| **Start stopped container** | `docker start legalbot-app` |
| **Restart container** | `docker restart legalbot-app` |
| **Interactive shell inside container** | `docker exec -it legalbot-app /bin/bash` |
| **Remove container** | `docker rm -f legalbot-app` |
| **Remove image** | `docker rmi legalbot:latest` |

---

## 8. Quick Troubleshooting

| Issue | Cause | Solution |
| :--- | :--- | :--- |
| **Port 8000 in use** | Local uvicorn or another app is running on port 8000. | Stop the local app, or map another host port: `-p 8080:8000`. |
| **Docker daemon not running** | Docker Desktop is closed. | Start Docker Desktop and wait until status shows "Engine running". |
| **API key not configured (503)** | Missing `--env-file .env` or empty keys. | Verify `.env` has `GEMINI_API_KEY` or `GROQ_API_KEY`, and add `--env-file .env`. |
| **Windows CRLF line endings** | `.env` has Windows line endings (`\r\n`). | Open `.env` in VS Code and change line endings to `LF`. |
| **Linux permission denied** | Non-root user not in docker group. | Run `sudo usermod -aG docker $USER && newgrp docker`. |
