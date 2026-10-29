"""Streamlit frontend for LegalBot — Indian legal assistant."""
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from app import config
from app.agents.legal_team import run_legal_workflow
from app.data.sample_documents import SAMPLE_LEGAL_DOCUMENTS

st.set_page_config(
    page_title="LegalBot — Indian Legal Assistant",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

with st.sidebar:
    st.title("⚖️ LegalBot")
    st.caption("Indian Legal Assistant")
    st.divider()

    st.subheader("System Status")
    is_ready = config.is_provider_configured()
    active_model = config.get_active_model_name()
    if is_ready:
        st.success(f"● Connected: {active_model}")
        st.caption(f"Provider: `{config.MODEL_PROVIDER.upper()}`")
    else:
        st.error(f"● {config.MODEL_PROVIDER.capitalize()} API key missing")
        if config.MODEL_PROVIDER == "google":
            st.info(
                "Add `GEMINI_API_KEY` to your `.env` file. "
                "[Google AI Studio](https://aistudio.google.com/apikey)"
            )
        else:
            st.info("Add `GROQ_API_KEY` to your `.env` file.")

    st.divider()
    st.subheader("Legal Analysis Workflow")
    st.markdown(
        """
        1. **Legal Query Analyzer**  
           Identifies the legal area, extracts facts, and frames key issues.

        2. **Legal Research Agent**  
           Searches the available legal library for relevant statutes and material.

        3. **Legal Answer Reviewer**  
           Reviews the response for consistency and synthesizes guidance.
        """
    )
    st.divider()
    with st.expander("📚 Available Legal Library", expanded=False):
        for doc in SAMPLE_LEGAL_DOCUMENTS:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"Category: {doc['category']}")
            st.caption(doc["summary"])
            st.markdown("---")

st.markdown(
    """
    <style>
    #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }
    header { background: transparent !important; }
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: flex !important;
        color: #93c5fd !important;
        z-index: 999999 !important;
    }
    .stApp { background-color: #0b0f19; color: #f8fafc; }
    .legal-banner {
        background-color: rgba(245, 158, 11, 0.08);
        border: 1px solid rgba(245, 158, 11, 0.25);
        color: #fde68a; padding: 10px 16px; border-radius: 6px;
        font-size: 0.88rem; margin-bottom: 20px;
    }
    .memo-card-header {
        background: #111827; border: 1px solid #1e293b;
        border-radius: 8px 8px 0 0; padding: 12px 18px;
        display: flex; justify-content: space-between; align-items: center;
        border-bottom: 2px solid #3b82f6; gap: 12px; flex-wrap: wrap;
    }
    .memo-tag {
        background-color: rgba(59, 130, 246, 0.15); color: #93c5fd;
        border: 1px solid rgba(59, 130, 246, 0.35); font-weight: 700;
        font-size: 0.75rem; padding: 2px 8px; border-radius: 4px;
        letter-spacing: 0.05em;
    }
    .audit-seal {
        background-color: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25); color: #34d399;
        padding: 10px 14px; border-radius: 6px; font-size: 0.84rem;
        font-weight: 600; margin-top: 18px; display: flex; align-items: center;
        gap: 8px;
    }
    .evidence-badge {
        background-color: rgba(99, 102, 241, 0.12);
        border: 1px solid rgba(99, 102, 241, 0.3); color: #c7d2fe;
        padding: 6px 12px; border-radius: 6px; font-size: 0.82rem;
        display: inline-flex; align-items: center; gap: 6px; margin: 12px 0;
    }
    .disclaimer-foot {
        color: #94a3b8; font-size: 0.78rem; line-height: 1.45; margin-top: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if "question_text" not in st.session_state:
    st.session_state.question_text = ""
if "response_data" not in st.session_state:
    st.session_state.response_data = None
if "attached_doc_name" not in st.session_state:
    st.session_state.attached_doc_name = None

st.title("Indian Legal Inquiry & Advisory")
st.markdown(
    '<div class="legal-banner"><strong>Notice:</strong> LegalBot provides '
    'legal information and statutory analysis under Indian law. It does not '
    'provide formal legal advice or representation. Verify applicable laws '
    'and consult a qualified advocate for advice about a specific matter.</div>',
    unsafe_allow_html=True,
)

st.write("**Common Indian Legal Scenarios**")
col1, col2 = st.columns(2)
with col1:
    if st.button("🏠 Tenancy Deposit Deduction", use_container_width=True):
        st.session_state.question_text = (
            "Can a residential landlord in Delhi deduct painting and cleaning "
            "charges from my security deposit without bills, and what rules "
            "may apply to the refund?"
        )
    if st.button("📄 Non-Compete Clause in India", use_container_width=True):
        st.session_state.question_text = (
            "Is a one-year post-employment non-compete clause in an IT "
            "employment contract enforceable in India under Section 27 of "
            "the Indian Contract Act?"
        )
with col2:
    if st.button("🔒 Mutual NDA and Confidentiality", use_container_width=True):
        st.session_state.question_text = (
            "What are common exclusions from confidentiality in a mutual "
            "non-disclosure agreement under Indian contract law?"
        )
    if st.button("🛒 E-Commerce Refund and Consumer Rights", use_container_width=True):
        st.session_state.question_text = (
            "What legal remedies may be available under the Consumer "
            "Protection Act, 2019, if an online seller refuses a refund "
            "for a defective laptop? Can I file a complaint online?"
        )

st.write("")
with st.form("inquiry_form"):
    user_query = st.text_area(
        "Enter your legal question or factual situation:",
        value=st.session_state.question_text,
        height=130,
        placeholder="Example: Can a landlord keep a security deposit without providing itemized repair bills?",
        max_chars=2000,
    )
    uploaded_image = st.file_uploader(
        "📷 Upload a document or agreement photo (optional)",
        type=["png", "jpg", "jpeg", "webp"],
        help="Attach a photo or scan of a rent agreement clause, NDA, termination letter, legal notice, invoice, or receipt.",
    )
    if uploaded_image:
        st.caption(
            f"📎 Attached file: `{uploaded_image.name}` "
            f"({uploaded_image.size // 1024} KB)"
        )
    btn_col1, btn_col2, _ = st.columns([1.5, 1, 4])
    with btn_col1:
        submitted = st.form_submit_button(
            "Analyze Legal Issue", type="primary", use_container_width=True
        )
    with btn_col2:
        cleared = st.form_submit_button("Clear", use_container_width=True)

if cleared:
    st.session_state.question_text = ""
    st.session_state.response_data = None
    st.session_state.attached_doc_name = None
    st.rerun()

if submitted:
    cleaned_query = user_query.strip()
    if not cleaned_query and not uploaded_image:
        st.error("Enter a legal question or upload a document photo.")
    elif cleaned_query and len(cleaned_query) < 5 and not uploaded_image:
        st.error("Please enter a legal question with at least 5 characters.")
    elif not config.is_provider_configured():
        st.error(
            f"The API key for {config.MODEL_PROVIDER.upper()} is not configured. "
            "Add it to your `.env` file and restart the application."
        )
    else:
        if not cleaned_query and uploaded_image:
            cleaned_query = (
                f"Examine the uploaded legal document ({uploaded_image.name}), "
                "identify key clauses, and provide legal analysis under Indian law."
            )
        st.session_state.question_text = cleaned_query
        st.session_state.attached_doc_name = uploaded_image.name if uploaded_image else None
        image_bytes = uploaded_image.getvalue() if uploaded_image else None
        image_name = uploaded_image.name if uploaded_image else None
        image_mime = uploaded_image.type if uploaded_image else None

        progress_placeholder = st.empty()
        with progress_placeholder.container():
            if image_bytes:
                st.info("Reviewing the uploaded document and analyzing the legal issue...")
            else:
                st.info("Analyzing the legal issue and preparing a response...")
        try:
            with st.spinner("Analyzing legal sources and preparing your response..."):
                st.session_state.response_data = run_legal_workflow(
                    cleaned_query,
                    image_bytes=image_bytes,
                    image_filename=image_name,
                    image_mime_type=image_mime,
                )
        except Exception:
            st.error(
                "The legal analysis could not be completed. Check your API "
                "configuration and application logs, then try again."
            )
        finally:
            progress_placeholder.empty()

if st.session_state.response_data:
    response = st.session_state.response_data
    answer_text = response.get("answer", "")
    sources = response.get("sources", [])
    st.write("---")
    st.markdown(
        """
        <div class="memo-card-header">
            <div>
                <span class="memo-tag">INDIAN LEGAL MEMORANDUM</span>
                <span style="font-size: 0.85rem; font-weight: 600; margin-left: 10px;">
                    Legal Analysis
                </span>
            </div>
            <div style="font-size: 0.78rem; opacity: 0.8;">
                Workflow: Analyze • Research • Review
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.session_state.attached_doc_name:
        safe_filename = (
            st.session_state.attached_doc_name
            .replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )
        st.markdown(
            '<div class="evidence-badge"><strong>📎 Analyzed document:</strong> '
            f"{safe_filename}</div>",
            unsafe_allow_html=True,
        )
    if sources:
        with st.expander(f"📚 Legal Sources Consulted ({len(sources)})", expanded=True):
            for source in sources:
                st.markdown(f"- **{source}**")
    st.markdown("### Legal Analysis")
    st.markdown(answer_text)
    st.markdown(
        """
        <div class="audit-seal">
            <span>✓</span>
            <span>Response prepared for informational purposes. Verify legal citations and applicability.</span>
        </div>
        <p class="disclaimer-foot">
            <strong>Disclaimer:</strong> LegalBot provides educational and
            informational guidance based on Indian law. This is not formal
            legal advice, legal representation, or an advocate-client
            relationship. Consult a qualified advocate for advice on a
            specific legal matter.
        </p>
        """,
        unsafe_allow_html=True,
    )
    evidence_note = (
        f"\nAttached document: {st.session_state.attached_doc_name}\n"
        if st.session_state.attached_doc_name else ""
    )
    st.download_button(
        label="Download Legal Memo (.txt)",
        data=(
            "INDIAN LEGAL MEMORANDUM\n\n"
            f"Question:\n{st.session_state.question_text}\n"
            f"{evidence_note}\nAnswer:\n{answer_text}\n\nSources:\n"
            + "\n".join(sources)
            + f"\n\n{config.LEGAL_DISCLAIMER}"
        ),
        file_name="indian_legal_memo.txt",
        mime="text/plain",
    )
