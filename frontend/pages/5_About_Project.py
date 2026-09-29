import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="About Project | ResponsibleMetrics AI",
    page_icon="📘",
    layout="wide"
)

# -------------------------------------------------
# THEME-ADAPTIVE CSS (PERFECT IN BOTH LIGHT & DARK MODE)
# -------------------------------------------------
st.markdown(
    """
    <style>
    .hero-title {
        font-size: 38px;
        font-weight: 800;
        margin-bottom: 8px;
        line-height: 1.2;
    }
    .hero-subtitle {
        font-size: 20px;
        opacity: 0.85;
        margin-bottom: 24px;
        line-height: 1.5;
    }
    .analogy-box {
        background: rgba(34, 197, 94, 0.12);
        border-left: 6px solid #22C55E;
        padding: 20px 24px;
        border-radius: 12px;
        font-size: 17px;
        margin-bottom: 24px;
        line-height: 1.6;
    }
    .problem-card {
        background: rgba(239, 68, 68, 0.10);
        border: 1px solid rgba(239, 68, 68, 0.35);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }
    .solution-card {
        background: rgba(59, 130, 246, 0.10);
        border: 1px solid rgba(59, 130, 246, 0.35);
        border-radius: 12px;
        padding: 18px 20px;
        margin-bottom: 16px;
    }
    .level-card {
        background: rgba(148, 163, 184, 0.10);
        border: 1px solid rgba(148, 163, 184, 0.30);
        border-radius: 12px;
        padding: 18px;
        height: 100%;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown('<div class="hero-title">📘 What is ResponsibleMetrics AI?</div>', unsafe_allow_html=True)
st.markdown(
    """
    <div class="hero-subtitle">
    An intelligent AI platform that ensures scientific research papers and scientists are evaluated 
    <b>fairly, responsibly, and without metric bias</b>.
    </div>
    """,
    unsafe_allow_html=True
)

# -------------------------------------------------
# SIMPLE REAL-WORLD ANALOGY (EASY TO UNDERSTAND)
# -------------------------------------------------
st.markdown(
    """
    <div class="analogy-box">
        💡 <b>Think of it like this:</b><br>
        Imagine judging whether a movie is good <i>solely</i> by how many tickets it sold in week one, 
        or judging an athlete's skill <i>solely</i> by their height. That would be unfair and misleading, right?<br><br>
        Yet in the scientific world, researchers and their life's work are often judged 
        <b>solely by a single number</b>—such as raw citation counts or the prestige of a journal name. 
        <b>ResponsibleMetrics AI is built to fix this problem.</b>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# -------------------------------------------------
# THE PROBLEM VS THE SOLUTION
# -------------------------------------------------
col_prob, col_sol = st.columns(2)

with col_prob:
    st.header("⚠️ The Real-World Problem")
    st.write("Today's scientific evaluation suffers from three major traps:")

    st.markdown(
        """
        <div class="problem-card">
            <h4>1. 🚫 Comparing Apples to Oranges</h4>
            <p>A medicine paper might naturally get 200 citations in a year because tens of thousands of researchers cite medical studies. 
            Meanwhile, an award-winning pure mathematics paper might only receive 5 citations because fewer researchers work in that specialized niche. 
            Comparing their raw citation numbers directly is completely invalid.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="problem-card">
            <h4>2. 🏷️ The "Journal Name" Trap (DORA Violation)</h4>
            <p>Evaluators often assume that if a paper is published in a famous journal (like <i>Nature</i> or <i>Science</i>), 
            the paper must be exceptional. In reality, citation distributions are heavily skewed: 80% of citations come from just 20% of articles. 
            Judging an individual paper by its journal name violates the <b>DORA declaration</b>.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="problem-card">
            <h4>3. 👶 Hurting Early-Career Researchers</h4>
            <p>Using cumulative lifelong numbers (like the <b>h-index</b>) automatically penalizes junior scientists, 
            PhD graduates, and researchers returning from family leaves who simply haven't had decades to amass citations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with col_sol:
    st.header("✨ How ResponsibleMetrics AI Solves It")
    st.write("Our platform reads papers like a responsible scientometric expert:")

    st.markdown(
        """
        <div class="solution-card">
            <h4>1. 🧠 Smart Natural Language Processing (NLP)</h4>
            <p>Rather than just counting citations, the AI reads the paper to understand its actual scientific contributions, 
            research questions, and methodology using <b>KeyBERT & dense Sentence Transformers</b>.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="solution-card">
            <h4>2. 🚨 Misuse & Red Flag Detection</h4>
            <p>The system audits paper rhetoric against internationally recognized guidelines (the <b>Leiden Manifesto</b> and <b>DORA</b>). 
            If metrics are misused (such as using Journal Impact Factor for individual evaluation), the system flags the exact violation and provides a scientific remedy.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="solution-card">
            <h4>3. 🧬 Real Literature Landscape & Research Gap</h4>
            <p>The AI compares the uploaded paper against a live open database (<b>OpenAlex</b>) 
            and projects it onto an interactive 2D cluster map to show where the work fits and what frontier gap it explores.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------
# HOW IT WORKS (IN 3 SIMPLE STEPS)
# -------------------------------------------------
st.header("🚀 How It Works in 3 Simple Steps")

step1, step2, step3 = st.columns(3)

with step1:
    st.subheader("1. 📄 Upload PDF")
    st.write(
        "Upload any scientific paper in PDF format. "
        "The system extracts sections (Abstract, Methodology, Findings) within seconds."
    )

with step2:
    st.subheader("2. 🤖 AI Analysis")
    st.write(
        "Our backend runs dense semantic embeddings, stance classifiers, and OpenAlex bibliometric lookup "
        "to audit how indicators are applied."
    )

with step3:
    st.subheader("3. 📊 Get Audit Report")
    st.write(
        "Receive a transparent scorecard showing Leiden/DORA compliance, "
        "detected red flags, literature gap positioning, and a downloadable formal audit certificate."
    )

st.divider()

# -------------------------------------------------
# THE 4 EVALUATION LEVELS EXPLAINED SIMPLY
# -------------------------------------------------
st.header("🏛️ The 4-Level Evaluation Framework")
st.write("Responsible research evaluation occurs across multiple levels of scientific organization:")

lvl1, lvl2, lvl3, lvl4 = st.columns(4)

with lvl1:
    st.markdown(
        """
        <div class="level-card">
            <h4>Level 1: Indicator</h4>
            <p><b>Focus:</b> The Metrics Themselves</p>
            <p>Are we using a healthy mix of indicators rather than a single number? Are limitations and margins of error stated?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with lvl2:
    st.markdown(
        """
        <div class="level-card">
            <h4>Level 2: Researcher</h4>
            <p><b>Focus:</b> The Individual Scientist</p>
            <p>Are early-career researchers evaluated fairly? Are qualitative portfolios and expert peer review prioritized over raw scores?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with lvl3:
    st.markdown(
        """
        <div class="level-card">
            <h4>Level 3: Institution</h4>
            <p><b>Focus:</b> Universities & Departments</p>
            <p>Are citation metrics normalized by academic discipline (e.g. FWCI)? Does evaluation reflect the university's research mission?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

with lvl4:
    st.markdown(
        """
        <div class="level-card">
            <h4>Level 4: System</h4>
            <p><b>Focus:</b> Global Policy & Science</p>
            <p>Is citation data open, transparent, and reproducible (via OpenAlex) rather than trapped in closed commercial silos?</p>
        </div>
        """,
        unsafe_allow_html=True
    )

st.divider()

# -------------------------------------------------
# MATHEMATICAL FORMULATIONS & SCORE DERIVATIONS
# -------------------------------------------------
st.header("📐 How Metrics Are Calculated (Mathematical Formulations)")
st.write(
    "ResponsibleMetrics AI combines rule-based scientometric auditing, OpenAlex bibliometric verification, "
    "and dense neural embeddings (`all-MiniLM-L6-v2`) to derive four primary evaluation indicators."
)

math_tab1, math_tab2, math_tab3, math_tab4 = st.tabs([
    "🏆 Responsible Score",
    "⚖️ Principle Compliance",
    "🔍 Literature Similarity",
    "💡 Novelty Level & Index"
])

with math_tab1:
    st.subheader("1. Responsible Score ($S_{\\text{resp}} \\in [0, 100]$)")
    st.latex(r"S_{\text{resp}} = \min\left(100, \sum_{d=1}^6 w_d \cdot D_d + B_{\text{biblio}}\right)")
    st.markdown(
        """
        The **Responsible Score** measures how comprehensively a research manuscript adheres to responsible scientometric reporting across six core Leiden dimensions:
        """
    )
    col_d1, col_d2 = st.columns(2)
    with col_d1:
        st.markdown(
            """
            * **Contextual Evaluation ($w_1 = 0.20$):** Qualitative explanations contextualizing quantitative numbers.
            * **Limitations Awareness ($w_2 = 0.20$):** Explicit caveats on metric bias, sample bounds, or margins of error.
            * **Methodological Transparency ($w_3 = 0.15$):** Reproducible calculation details, code/data access.
            """
        )
    with col_d2:
        st.markdown(
            """
            * **Metric Diversity ($w_4 = 0.15$):** Using an indicator portfolio rather than a single metric.
            * **Qualitative Evidence ($w_5 = 0.15$):** Incorporating expert peer review or narrative evidence.
            * **Discipline Awareness ($w_6 = 0.15$):** Field-normalized comparisons (e.g., FWCI or subfield percentiles).
            """
        )
    st.markdown(
        """
        - **Dimension Score:** $D_d = \\min\\left(100, \\frac{\\text{matches}_d}{\\text{max\\_matches}_d} \\times 100\\right)$ based on matched NLP rhetorical indicators.
        - **Metadata Bonus ($B_{\\text{biblio}} \\le 5$):** OpenAlex verified metadata bonus (+2 citations, +1 publication year, +2 open access).
        """
    )

with math_tab2:
    st.subheader("2. Principle Compliance Score ($S_{\\text{comp}} \\in [0, 100]$)")
    st.latex(r"S_{\text{comp}} = \max\left(0, \min\left(100, 50 + 7 \cdot |P| - \sum_{m \in M} \text{penalty}(m)\right)\right)")
    st.markdown(
        """
        The **Principle Compliance Score** measures strict adherence to the **Leiden Manifesto** and **DORA** declarations, starting from an unbiased baseline of **50%**:
        - **Positive Compliance Reward ($+7\\%$ per detected practice):**
          - Supporting qualitative judgment (Leiden P1).
          - Field-normalized citation evaluation (Leiden P6).
          - Indicator portfolio transparency (Leiden P9).
          - Article-level evaluation avoiding journal-level proxies (DORA).
        - **Deductive Penalties by Misuse Severity:**
          - **High Severity ($-15\\%$):** Using Journal Impact Factor (JIF) to judge individual papers/researchers, single-metric gatekeeping, unnormalized cross-discipline comparisons.
          - **Medium Severity ($-10\\%$):** Arbitrary h-index cutoffs or metric gaming without context.
          - **Low Severity ($-5\\%$):** False precision (e.g. reporting impact factors to 3 decimal places).
        """
    )

with math_tab3:
    st.subheader("3. Literature Similarity (Cosine Similarity $\\bar{S}$)")
    st.latex(r"\text{Sim}(q, d_i) = \frac{\vec{v}_q \cdot \vec{v}_i}{\|\vec{v}_q\|_2 \|\vec{v}_i\|_2}")
    st.latex(r"\bar{S} = \frac{1}{N}\sum_{i=1}^N \text{Sim}(q, d_i)")
    st.markdown(
        """
        - The uploaded paper $q$ and benchmark corpus documents $d_i$ are mapped into a dense 384-dimensional semantic embedding space using **Sentence-BERT** (`all-MiniLM-L6-v2`).
        - **Nearest Prior Art Match:** $\\text{Sim}_{\\text{nearest}} = \\max_i \\text{Sim}(q, d_i)$ identifies the most conceptually similar published work.
        - **Literature Similarity (Average):** $\\bar{S}$ reflects the overall contextual alignment across the benchmark corpus ($N=20$). High values indicate core mainstream bibliometric topics; lower values indicate emerging or interdisciplinary domains.
        """
    )

with math_tab4:
    st.subheader("4. Novelty Level & Novelty Index ($N_{\\text{index}} \\in [0\\%, 100\\%]$)")
    st.latex(r"\text{Overlap} = 0.60 \cdot s_{\text{top1}} + 0.40 \cdot s_{\text{top3}}")
    st.latex(r"N_{\text{score}} = 0.70 \cdot (1.0 - \text{Overlap}) + 0.30 \cdot (1.0 - s_{\text{cluster}})")
    st.latex(r"N_{\text{index}} = N_{\text{score}} \times 100\%")
    st.markdown(
        """
        Novelty quantifies how much the paper departs from existing literature to explore an unfilled research gap:
        - **Overlap Metric:** Blends nearest prior art similarity ($s_{\\text{top1}}$) with local neighborhood density ($s_{\\text{top3}}$) to prevent single-outlier distortion.
        - **Cluster Distance ($1.0 - s_{\\text{cluster}}$):** Measures semantic distance from the closest K-Means literature cluster centroid.
        - **Calibrated Novelty Thresholds:**
          - 🚀 **High Novelty ($N_{\\text{index}} \\ge 72\\%$):** *Frontier / Pioneering Work.* Low overlap with existing corpus, addressing novel questions or unstudied domains.
          - ⚖️ **Medium Novelty ($42\\% \\le N_{\\text{index}} < 72\\%$):** *Novel Synthesis / Extension.* Extends established methodologies to new contexts or combines multiple subfields.
          - 📚 **Low Novelty ($N_{\\text{index}} < 42\\%$):** *Incremental Addition.* High overlap ($s > 0.60$) with existing dense literature clusters.
        """
    )

st.divider()

# -------------------------------------------------
# WHO IS THIS BUILT FOR?
# -------------------------------------------------
st.header("👥 Who Can Use This System?")

col_u1, col_u2, col_u3, col_u4 = st.columns(4)

with col_u1:
    st.markdown("### 🎓 Students & Authors")
    st.write("Understand how papers are assessed and ensure citations and metric references follow responsible scientific standards.")

with col_u2:
    st.markdown("### 🏛️ University Committees")
    st.write("Conduct fair faculty hiring, tenure, and promotion reviews without relying on misleading metric shortcuts.")

with col_u3:
    st.markdown("### 📖 Journal Editors")
    st.write("Screen manuscripts during peer review to verify citation rigor and adherence to DORA principles.")

with col_u4:
    st.markdown("### 💰 Funding Agencies")
    st.write("Award research grants based on genuine scientific merit rather than superficial journal brand names.")

st.divider()

# -------------------------------------------------
# FREQUENTLY ASKED QUESTIONS (FAQ)
# -------------------------------------------------
st.header("❓ Frequently Asked Questions")

with st.expander("Does this AI replace human peer review?"):
    st.write(
        "**No, absolutely not!** Principle 1 of the Leiden Manifesto explicitly dictates that quantitative metrics "
        "must *support* human qualitative peer review, never replace it. ResponsibleMetrics AI serves as an "
        "auditing companion that helps human experts spot metric misuse, gaming, and unnormalized comparisons."
    )

with st.expander("What are DORA and the Leiden Manifesto?"):
    st.markdown(
        """
        They are the two leading international scientific declarations for fair research assessment:
        * **DORA (San Francisco Declaration, 2012):** Urges scientific institutions worldwide to stop using Journal Impact Factor as a shortcut to evaluate individual researchers.
        * **The Leiden Manifesto (Nature, 2015):** 10 golden principles outlining how metrics must be transparent, field-normalized, and subordinate to qualitative expert judgment.
        """
    )

with st.expander("Where does the citation and paper data come from?"):
    st.write(
        "ResponsibleMetrics AI connects directly to **OpenAlex**, a comprehensive and open catalog of the global research system. "
        "Unlike closed proprietary databases, OpenAlex is open-access, verifiable, and transparent."
    )

st.caption("ResponsibleMetrics AI | Final Year Project in Information Retrieval & Natural Language Processing (IRNLP)")