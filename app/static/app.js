/**
 * LegalBot Frontend Client Logic
 * Refined, reliable, and clean.
 */

document.addEventListener("DOMContentLoaded", () => {
  // Elements
  const form = document.getElementById("legalForm");
  const questionInput = document.getElementById("questionInput");
  const charCount = document.getElementById("charCount");
  const submitBtn = document.getElementById("submitBtn");
  const clearBtn = document.getElementById("clearBtn");
  const copyBtn = document.getElementById("copyBtn");

  const systemStatus = document.getElementById("systemStatus");
  const statusLabel = document.getElementById("statusLabel");
  const modelTag = document.getElementById("modelTag");

  const emptyView = document.getElementById("emptyView");
  const loadingView = document.getElementById("loadingView");
  const loadingLabel = document.getElementById("loadingLabel");
  const loadingCaption = document.getElementById("loadingCaption");

  const errorView = document.getElementById("errorView");
  const errorMsg = document.getElementById("errorMsg");

  const responseView = document.getElementById("responseView");
  const sourcesBlock = document.getElementById("sourcesBlock");
  const sourcesTags = document.getElementById("sourcesTags");
  const answerArticle = document.getElementById("answerArticle");
  const disclaimerNotice = document.getElementById("disclaimerNotice");

  const pipe1 = document.getElementById("pipe1");
  const pipe2 = document.getElementById("pipe2");
  const pipe3 = document.getElementById("pipe3");

  const printBtn = document.getElementById("printBtn");
  const memoTimestamp = document.getElementById("memoTimestamp");

  let latestAnswerRaw = "";
  let pipelineTimer = null;

  // Initialize
  verifyBackendStatus();

  // Character counter
  questionInput.addEventListener("input", () => {
    charCount.textContent = questionInput.value.length;
  });

  // Suggestion chips
  document.querySelectorAll(".suggestion-chip").forEach((btn) => {
    btn.addEventListener("click", () => {
      questionInput.value = btn.getAttribute("data-query");
      charCount.textContent = questionInput.value.length;
      questionInput.focus();
    });
  });

  // Clear button
  clearBtn.addEventListener("click", () => {
    questionInput.value = "";
    charCount.textContent = "0";
    resetPipelineSteps();
    hideError();
    responseView.style.display = "none";
    copyBtn.style.display = "none";
    if (printBtn) printBtn.style.display = "none";
    emptyView.style.display = "flex";
    questionInput.focus();
  });

  // Print button
  if (printBtn) {
    printBtn.addEventListener("click", () => {
      window.print();
    });
  }

  // Copy button
  copyBtn.addEventListener("click", async () => {
    if (!latestAnswerRaw) return;
    try {
      await navigator.clipboard.writeText(latestAnswerRaw);
      const span = copyBtn.querySelector("span");
      const prev = span.textContent;
      span.textContent = "Copied!";
      setTimeout(() => {
        span.textContent = prev;
      }, 1800);
    } catch (e) {
      console.error("Copy failed", e);
    }
  });

  // Form submission
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const query = questionInput.value.trim();

    if (!query || query.length < 5) {
      showError("Please enter a question with at least 5 characters.");
      return;
    }

    startSubmission();

    try {
      const response = await fetch("/ask", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: query }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || `Server error (${response.status})`);
      }

      renderResponse(data);
    } catch (err) {
      showError(err.message || "Failed to communicate with LegalBot backend.");
    } finally {
      stopSubmission();
    }
  });

  // Health check
  async function verifyBackendStatus() {
    try {
      const res = await fetch("/health");
      if (!res.ok) throw new Error("Health check non-200");
      const data = await res.json();

      const dot = systemStatus.querySelector(".status-dot");
      dot.className = "status-dot active";

      if (data.groq_configured) {
        statusLabel.textContent = "Backend Ready";
      } else {
        statusLabel.textContent = "API Key Missing (.env)";
        showError("Groq API Key is not set! Please add GROQ_API_KEY in your .env file.");
      }

      if (data.model) {
        modelTag.textContent = data.model;
      }
    } catch (err) {
      const dot = systemStatus.querySelector(".status-dot");
      dot.className = "status-dot inactive";
      statusLabel.textContent = "Offline";
    }
  }

  // Multi-agent pipeline animation
  function startPipelineAnimation() {
    resetPipelineSteps();
    const stages = [
      {
        el: pipe1,
        title: "Legal Query Analyzer Active...",
        caption: "Classifying inquiry, extracting facts, and formulating legal issues.",
      },
      {
        el: pipe2,
        title: "Legal Research Agent Active...",
        caption: "Querying statutory standards, contract samples, and citations.",
      },
      {
        el: pipe3,
        title: "Legal Answer Reviewer Active...",
        caption: "Auditing assertions, eliminating unsupported claims, and formatting output.",
      },
    ];

    let current = 0;
    function advance() {
      resetPipelineSteps();
      const st = stages[current];
      if (st && st.el) {
        st.el.classList.add("active");
        loadingLabel.textContent = st.title;
        loadingCaption.textContent = st.caption;
      }
      current = (current + 1) % stages.length;
    }

    advance();
    pipelineTimer = setInterval(advance, 3500);
  }

  function resetPipelineSteps() {
    [pipe1, pipe2, pipe3].forEach((el) => {
      if (el) el.classList.remove("active");
    });
  }

  function completePipelineSteps() {
    if (pipelineTimer) {
      clearInterval(pipelineTimer);
      pipelineTimer = null;
    }
    [pipe1, pipe2, pipe3].forEach((el) => {
      if (el) el.classList.add("active");
    });
  }

  // Submission state helpers
  function startSubmission() {
    hideError();
    emptyView.style.display = "none";
    responseView.style.display = "none";
    copyBtn.style.display = "none";
    if (printBtn) printBtn.style.display = "none";
    loadingView.style.display = "flex";

    submitBtn.disabled = true;
    startPipelineAnimation();
  }

  function stopSubmission() {
    loadingView.style.display = "none";
    submitBtn.disabled = false;
    completePipelineSteps();
  }

  function renderResponse(data) {
    hideError();
    emptyView.style.display = "none";
    responseView.style.display = "flex";
    copyBtn.style.display = "inline-flex";
    if (printBtn) printBtn.style.display = "inline-flex";

    if (memoTimestamp) {
      const now = new Date();
      memoTimestamp.textContent = now.toLocaleDateString(undefined, {
        month: "short",
        day: "numeric",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit",
      });
    }

    latestAnswerRaw = data.answer || "";
    answerArticle.innerHTML = renderMarkdown(latestAnswerRaw);

    // Citations
    if (data.sources && Array.isArray(data.sources) && data.sources.length > 0) {
      sourcesTags.innerHTML = "";
      data.sources.forEach((src) => {
        const span = document.createElement("span");
        span.className = "source-tag";
        span.textContent = src;
        sourcesTags.appendChild(span);
      });
      sourcesBlock.style.display = "block";
    } else {
      sourcesBlock.style.display = "none";
    }

    disclaimerNotice.textContent = data.disclaimer || "";
  }

  function showError(msg) {
    errorMsg.textContent = msg;
    errorView.style.display = "flex";
  }

  function hideError() {
    errorView.style.display = "none";
  }

  // Safe markdown parser
  function renderMarkdown(md) {
    if (!md) return "";

    let safe = md
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");

    safe = safe.replace(/^### (.*$)/gim, "<h3>$1</h3>");
    safe = safe.replace(/^## (.*$)/gim, "<h2>$1</h2>");
    safe = safe.replace(/^# (.*$)/gim, "<h1>$1</h1>");

    safe = safe.replace(/\*\*\*(.*?)\*\*\*/gim, "<strong><em>$1</em></strong>");
    safe = safe.replace(/\*\*(.*?)\*\*/gim, "<strong>$1</strong>");
    safe = safe.replace(/\*(.*?)\*/gim, "<em>$1</em>");
    safe = safe.replace(/`([^`]+)`/gim, "<code>$1</code>");
    safe = safe.replace(/^\> (.*$)/gim, "<blockquote>$1</blockquote>");

    const lines = safe.split("\n");
    let inList = false;
    const result = [];

    for (let i = 0; i < lines.length; i++) {
      let line = lines[i].trim();
      if (line.startsWith("- ") || line.startsWith("* ")) {
        if (!inList) {
          result.push("<ul>");
          inList = true;
        }
        result.push(`<li>${line.substring(2)}</li>`);
      } else {
        if (inList) {
          result.push("</ul>");
          inList = false;
        }
        if (line && !line.startsWith("<h") && !line.startsWith("<blockquote") && !line.startsWith("<ul")) {
          result.push(`<p>${line}</p>`);
        } else if (line) {
          result.push(line);
        }
      }
    }

    if (inList) {
      result.push("</ul>");
    }

    return result.join("\n");
  }
});
