import streamlit as st

from utils.api import check_backend


st.set_page_config(

    page_title="ResponsibleMetrics AI",

    page_icon="📊",

    layout="wide",

    initial_sidebar_state="expanded"
)


# -------------------------------
# CUSTOM CSS
# -------------------------------

st.markdown(

    """
    <style>

    .main-title {
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 0px;
        line-height: 1.2;
    }

    .subtitle {
        font-size: 18px;
        opacity: 0.85;
        margin-bottom: 30px;
    }

    .feature-card {
        padding: 20px;
        border-radius: 12px;
        background: rgba(148, 163, 184, 0.08);
        border: 1px solid rgba(148, 163, 184, 0.25);
        min-height: 180px;
    }

    </style>
    """,

    unsafe_allow_html=True
)


# -------------------------------
# SIDEBAR
# -------------------------------

with st.sidebar:

    st.title("ResponsibleMetrics AI")

    st.divider()

    backend_status = check_backend()


    if backend_status and not backend_status.get("error") and backend_status.get("status") == "healthy":

        st.success(
            "Backend Connected"
        )

    else:

        st.error(
            "Backend Offline"
        )


# -------------------------------
# MAIN PAGE
# -------------------------------

st.markdown(

    '<div class="main-title">ResponsibleMetrics AI</div>',

    unsafe_allow_html=True
)


st.markdown(

    """
    <div class="subtitle">
    An NLP-Based Multi-Level Framework for Responsible
    Use of Bibliometric Indicators
    </div>
    """,

    unsafe_allow_html=True
)


st.divider()


# -------------------------------
# PROJECT OVERVIEW
# -------------------------------

st.subheader(
    "Research Paper Evaluation Platform"
)


st.write(

    """
    ResponsibleMetrics AI analyzes research papers using
    Natural Language Processing, bibliometric indicators,
    responsible research assessment principles, and
    research gap detection.
    """
)


# -------------------------------
# FEATURES
# -------------------------------

col1, col2, col3 = st.columns(3)


with col1:

    st.markdown(

        """
        <div class="feature-card">

        <h3>📄 Paper Analysis</h3>

        Upload a research paper and automatically
        extract important research information.

        </div>
        """,

        unsafe_allow_html=True
    )


with col2:

    st.markdown(

        """
        <div class="feature-card">

        <h3>📊 Responsible Metrics</h3>

        Evaluate the responsible use of bibliometric
        indicators using research assessment principles.

        </div>
        """,

        unsafe_allow_html=True
    )


with col3:

    st.markdown(

        """
        <div class="feature-card">

        <h3>🔍 Research Gap Detection</h3>

        Identify potential underexplored research areas
        using semantic similarity analysis.

        </div>
        """,

        unsafe_allow_html=True
    )


st.divider()


# -------------------------------
# SYSTEM MODULES
# -------------------------------

st.subheader(
    "System Capabilities"
)


col1, col2 = st.columns(2)


with col1:

    st.write("✓ PDF Research Paper Upload")

    st.write("✓ NLP-Based Text Analysis")

    st.write("✓ Bibliometric Data Integration")

    st.write("✓ Responsible Metrics Evaluation")


with col2:

    st.write("✓ Principle & Misuse Detection")

    st.write("✓ Research Gap Detection")

    st.write("✓ Analysis History")

    st.write("✓ Explainable Research Evaluation")


st.divider()


st.caption(

    "ResponsibleMetrics AI | Research Evaluation System"
)