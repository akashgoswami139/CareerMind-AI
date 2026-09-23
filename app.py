import json
import html
import textwrap
import streamlit as st

from rag_chain import run_rag


def render_html(markup: str) -> None:
    """Render an HTML block via st.markdown without it being
    mis-parsed as a Markdown code block (which happens when the
    lines carry leading indentation)."""
    st.markdown(textwrap.dedent(markup).strip(), unsafe_allow_html=True)


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="CareerMind AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CUSTOM CSS — LIGHT / ANIMATED THEME
# =========================================================

st.markdown(
    """
    <style>

    /* ---------- Keyframes ---------- */

    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(14px); }
        to   { opacity: 1; transform: translateY(0); }
    }

    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }

    @keyframes pulseGlow {
        0%, 100% { box-shadow: 0 0 0 rgba(99, 102, 241, 0.0); }
        50%      { box-shadow: 0 0 22px rgba(99, 102, 241, 0.18); }
    }

    @keyframes shimmer {
        0%   { background-position: -400px 0; }
        100% { background-position: 400px 0; }
    }

    /* ---------- Global ---------- */

    .stApp {
        background: #f7f8fb;
    }

    .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* ---------- Header ---------- */

    .hero {
        padding: 14px 0 28px 0;
        animation: fadeInUp 0.6s ease-out;
    }

    .hero-title {
        font-size: 44px;
        font-weight: 800;
        line-height: 1.1;
        letter-spacing: -1px;
        margin: 0;
        background: linear-gradient(90deg, #4f46e5, #7c3aed, #ec4899, #4f46e5);
        background-size: 300% 300%;
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        animation: gradientShift 6s ease infinite;
    }

    .hero-subtitle {
        font-size: 16px;
        color: #667085;
        margin-top: 10px;
    }

    /* ---------- Cards ---------- */

    .glass-card {
        background: #ffffff;
        border: 1px solid #e7e9f0;
        border-radius: 16px;
        padding: 20px;
        margin: 8px 0 16px 0;
        box-shadow: 0 4px 18px rgba(17, 24, 39, 0.05);
        animation: fadeInUp 0.5s ease-out;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .glass-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 26px rgba(17, 24, 39, 0.09);
    }

    .section-title {
        font-size: 20px;
        font-weight: 700;
        color: #111827;
        margin: 8px 0 12px 0;
    }

    /* ---------- Skill Cards ---------- */

    .skill-card {
        background: #ffffff;
        border: 1px solid #e7e9f0;
        border-left: 3px solid #6366f1;
        border-radius: 14px;
        padding: 16px 18px;
        margin-bottom: 10px;
        box-shadow: 0 2px 10px rgba(17, 24, 39, 0.04);
        animation: fadeInUp 0.45s ease-out;
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-left-color 0.2s ease;
    }

    .skill-card:hover {
        transform: translateX(4px);
        box-shadow: 0 6px 18px rgba(99, 102, 241, 0.12);
        border-left-color: #ec4899;
    }

    .skill-name {
        color: #111827;
        font-size: 17px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .skill-meta {
        color: #667085;
        font-size: 13px;
        line-height: 1.6;
    }

    .skill-value {
        color: #4338ca;
        font-weight: 700;
    }

    /* ---------- Summary ---------- */

    .summary-text {
        color: #374151;
        font-size: 15px;
        line-height: 1.75;
    }

    /* ---------- Buttons ---------- */

    .stButton > button {
        border-radius: 10px !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(99, 102, 241, 0.25);
    }

    div[data-testid="stFormSubmitButton"] button,
    .stButton > button[kind="primary"] {
        background: linear-gradient(90deg, #4f46e5, #7c3aed) !important;
        border: none !important;
        animation: pulseGlow 2.4s ease-in-out infinite;
    }

    /* ---------- Metrics ---------- */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e7e9f0;
        border-radius: 14px;
        padding: 12px 14px;
        box-shadow: 0 2px 10px rgba(17, 24, 39, 0.04);
        transition: transform 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-2px);
    }

    /* ---------- Footer ---------- */

    .built-by {
        position: fixed;
        left: 16px;
        bottom: 12px;
        z-index: 999999;
        background: rgba(255, 255, 255, 0.92);
        border: 1px solid #e7e9f0;
        border-radius: 10px;
        padding: 7px 11px;
        color: #667085;
        font-size: 12px;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 14px rgba(17, 24, 39, 0.06);
    }

    .built-by b {
        color: #111827;
    }

    /* ---------- Sidebar ---------- */

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid #e7e9f0;
    }

    /* ---------- Text input ---------- */

    .stTextInput input {
        border-radius: 10px !important;
        border: 1px solid #d9dce3 !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    .stTextInput input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15) !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# SESSION STATE
# =========================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "last_query" not in st.session_state:
    st.session_state.last_query = ""


# =========================================================
# HEADER
# =========================================================

render_html(
    """
    <div class="hero">
        <div class="hero-title">🎯 CareerMind AI</div>
        <div class="hero-subtitle">
            AI-powered job analysis using RAG, ChromaDB, Jina Embeddings and Gemini
        </div>
    </div>
    """
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("## CareerMind AI")

    st.write(
        "Analyze job roles from your knowledge base and extract "
        "important skills, priorities, evidence and salary information."
    )

    st.divider()

    st.markdown("### ⚙️ Stack")

    st.write("🔹 LangChain")
    st.write("🔹 ChromaDB")
    st.write("🔹 Jina Embeddings")
    st.write("🔹 Gemini")
    st.write("🔹 Streamlit")

    st.divider()

    st.markdown("### 📌 Example Queries")

    example_queries = [
        "Machine Learning",
        "Data Scientist",
        "AI Engineer",
        "Python Developer",
        "MLOps Engineer",
    ]

    for example in example_queries:
        if st.button(example, key=f"example_{example}"):
            st.session_state.last_query = example
            st.session_state.result = None
            st.rerun()


# =========================================================
# INPUT
# =========================================================

render_html('<div class="section-title">🔎 Analyze Job Role</div>')

query = st.text_input(
    "Job Role",
    value=st.session_state.last_query,
    placeholder="Example: Machine Learning",
    label_visibility="collapsed",
)


# =========================================================
# BUTTONS
# =========================================================

col1, col2 = st.columns([4, 1])

with col1:
    analyze_clicked = st.button(
        "🚀 Analyze",
        type="primary",
        use_container_width=True,
    )

with col2:
    clear_clicked = st.button(
        "🗑️ Clear",
        use_container_width=True,
    )


if clear_clicked:
    st.session_state.result = None
    st.session_state.last_query = ""
    st.rerun()


# =========================================================
# RUN RAG
# =========================================================

if analyze_clicked:

    if not query.strip():
        st.warning("Please enter a job role.")
    else:

        st.session_state.last_query = query

        with st.spinner("🔍 Retrieving documents and analyzing..."):

            try:
                raw_result = run_rag(query.strip())

                # ---------------------------------------------
                # Normalize Gemini response
                # ---------------------------------------------

                result_text = raw_result

                if isinstance(raw_result, list):

                    text_parts = []

                    for item in raw_result:

                        if isinstance(item, dict):

                            if item.get("type") == "text":
                                text_parts.append(
                                    item.get("text", "")
                                )

                        elif isinstance(item, str):
                            text_parts.append(item)

                    result_text = "".join(text_parts)

                elif hasattr(raw_result, "content"):

                    result_text = raw_result.content

                # ---------------------------------------------
                # Parse JSON
                # ---------------------------------------------

                if isinstance(result_text, str):

                    cleaned = result_text.strip()

                    # Remove markdown JSON fences if Gemini adds them
                    if cleaned.startswith("```json"):
                        cleaned = cleaned[7:]

                    if cleaned.startswith("```"):
                        cleaned = cleaned[3:]

                    if cleaned.endswith("```"):
                        cleaned = cleaned[:-3]

                    cleaned = cleaned.strip()

                    try:
                        parsed_result = json.loads(cleaned)

                    except json.JSONDecodeError:

                        # Try extracting the JSON object
                        start = cleaned.find("{")
                        end = cleaned.rfind("}")

                        if start != -1 and end != -1:
                            parsed_result = json.loads(
                                cleaned[start:end + 1]
                            )
                        else:
                            parsed_result = None

                elif isinstance(result_text, dict):
                    parsed_result = result_text

                else:
                    parsed_result = None

                st.session_state.result = parsed_result

            except Exception as error:

                st.error("Something went wrong while analyzing the job role.")
                st.exception(error)


# =========================================================
# DISPLAY RESULT
# =========================================================

result = st.session_state.result


if result:

    st.success("✅ Analysis completed successfully.")

    # =====================================================
    # JOB ROLE
    # =====================================================

    job_role = result.get("job_role", "Not available")

    render_html(
        f"""
        <div class="glass-card">
            <div class="section-title">🎯 Job Role</div>
            <div style="font-size: 24px; font-weight: 700; color: #111827;">
                {html.escape(str(job_role))}
            </div>
        </div>
        """
    )

    # =====================================================
    # SKILLS
    # =====================================================

    render_html('<div class="section-title">🧠 Required Skills</div>')

    skills = result.get("skills", [])

    if skills:

        for skill in skills:

            skill_name = skill.get("skill", "N/A")
            importance = skill.get("importance_percentage", 0)
            priority = skill.get("priority", "N/A")
            evidence = skill.get("evidence_count", 0)

            priority_text = html.escape(str(priority))
            skill_text = html.escape(str(skill_name))

            render_html(
                f"""
                <div class="skill-card">
                    <div class="skill-name">{skill_text}</div>
                    <div class="skill-meta">
                        Importance: <span class="skill-value">{importance}%</span>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Priority: <span class="skill-value">{priority_text}</span>
                        &nbsp;&nbsp;|&nbsp;&nbsp;
                        Evidence: <span class="skill-value">{evidence}</span>
                    </div>
                </div>
                """
            )

    else:

        st.info("No skills were found in the retrieved documents.")

    # =====================================================
    # SALARY
    # =====================================================

    render_html('<div class="section-title">💰 Salary Analysis</div>')

    salary = result.get("salary_analysis", {})

    average = salary.get("average_ctc_lpa")
    minimum = salary.get("minimum_ctc_lpa")
    maximum = salary.get("maximum_ctc_lpa")
    count = salary.get("salary_data_count", 0)
    confidence = salary.get("confidence", "Unknown")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Average CTC",
            f"{average} LPA" if average is not None else "N/A",
        )

    with col2:
        st.metric(
            "Minimum CTC",
            f"{minimum} LPA" if minimum is not None else "N/A",
        )

    with col3:
        st.metric(
            "Maximum CTC",
            f"{maximum} LPA" if maximum is not None else "N/A",
        )

    with col4:
        st.metric(
            "Salary Records",
            str(count),
        )

    st.caption(f"Confidence: {confidence}")

    # =====================================================
    # SUMMARY
    # =====================================================

    summary = result.get("summary", "")

    if summary:

        render_html('<div class="section-title">📝 Summary</div>')

        render_html(
            f"""
            <div class="glass-card">
                <div class="summary-text">
                    {html.escape(str(summary))}
                </div>
            </div>
            """
        )

    # =====================================================
    # RAW JSON
    # =====================================================

    with st.expander("🔧 View Raw JSON"):

        st.json(result)


elif not analyze_clicked:

    st.info(
        "Enter a job role above and click **Analyze** to start."
    )


# =========================================================
# FOOTER
# =========================================================

render_html(
    """
    <div class="built-by">
        <b>Akash Goswami</b>
    </div>
    """
)