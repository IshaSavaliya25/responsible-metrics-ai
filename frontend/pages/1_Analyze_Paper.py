import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import analyze_paper


# --------------------------------
# PAGE CONFIG
# --------------------------------

st.set_page_config(

    page_title="Analyze Paper | ResponsibleMetrics AI",

    page_icon="📄",

    layout="wide"
)


# --------------------------------
# TITLE
# --------------------------------

st.title("📄 Analyze Research Paper")

st.write(
    """
    Upload a research paper in PDF format. The system will analyze
    the paper using NLP, bibliometric indicators, responsible metrics,
    principle detection, and research gap detection.
    """
)

st.divider()


# --------------------------------
# FILE UPLOAD
# --------------------------------

uploaded_file = st.file_uploader(

    "Upload Research Paper (PDF)",

    type=["pdf"]
)


# --------------------------------
# ANALYZE BUTTON
# --------------------------------

if uploaded_file:

    st.success(
        f"Selected file: {uploaded_file.name}"
    )


    if st.button(

        "🚀 Analyze Paper",

        use_container_width=True,

        type="primary"
    ):

        with st.spinner(

            "Analyzing research paper... This may take a few moments."
        ):

            result = analyze_paper(
                uploaded_file
            )

        # Check backend response
        if not result or not isinstance(result, dict):
            st.error("❌ Failed to receive a valid response from the backend service.")
        elif result.get("duplicate") or (isinstance(result.get("error"), str) and "already been analyzed" in result.get("error", "").lower()):
            st.warning("⚠️ This research paper has already been analyzed.")
            err_msg = result.get("message") or result.get("error")
            if err_msg:
                st.info(err_msg)
            st.page_link(
                "pages/3_Analysis_History.py",
                label="📚 View Previous Analysis in History",
                icon="📚"
            )
        elif result.get("error"):
            st.error(f"❌ Analysis failed: {result['error']}")
        else:
            st.success("🎉 Paper analysis completed successfully!")
            st.session_state["analysis_result"] = result


# --------------------------------
# DISPLAY RESULTS
# --------------------------------

if "analysis_result" in st.session_state:

    result = st.session_state["analysis_result"]
    if not isinstance(result, dict) or result.get("error") or result.get("duplicate"):
        st.session_state.pop("analysis_result", None)
        st.stop()

    import json

    def to_dict(val):
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            try:
                parsed = json.loads(val)
                if isinstance(parsed, dict):
                    return parsed
                if isinstance(parsed, list):
                    return {"items": parsed}
            except Exception:
                return {}
        return {}

    # --------------------------------
    # PAPER INFORMATION
    # --------------------------------

    st.divider()

    st.header("📄 Paper Information")

    paper_info = to_dict(result.get("paper_information"))
    file_info = to_dict(result.get("file"))

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Pages",
            paper_info.get("page_count", "N/A")
        )


    with col2:

        st.metric(

            "Words",

            paper_info.get(
                "word_count",
                "N/A"
            )
        )


    with col3:

        st.metric(

            "Characters",

            paper_info.get(
                "character_count",
                "N/A"
            )
        )


    with col4:

        st.metric(

            "Database ID",

            result.get(
                "database_id",
                "N/A"
            )
        )


    st.write(
        "**Filename:**",
        file_info.get(
            "filename",
            "Unknown"
        )
    )


    st.write(
        "**Detected Title:**",
        paper_info.get(
            "detected_title",
            "Not detected"
        )
    )

    # --------------------------------
    # DETECTED PAPER STRUCTURE
    # --------------------------------

    st.divider()

    st.subheader("📑 Detected Paper Structure")

    sections = result.get(
        "sections_detected",
        []
    )

    if sections:

        columns = st.columns(4)

        for index, section in enumerate(sections):

            formatted_section = (
                section
                .replace("_", " ")
                .title()
            )

            with columns[index % 4]:

                st.success(
                    f"✓ {formatted_section}"
                )

    else:

        st.info(
            "No major sections detected."
        )


    # --------------------------------
    # OVERALL SCORES
    # --------------------------------

    st.divider()

    st.header("📊 Evaluation Overview")

    responsible_data = to_dict(result.get("responsible_metrics_evaluation")) or to_dict(result.get("responsible_metrics"))
    principle_data = to_dict(result.get("principle_analysis"))
    gap_data = to_dict(result.get("research_gap_analysis"))
    nlp_data = to_dict(result.get("nlp_analysis"))
    bibliometric_data = to_dict(result.get("bibliometric_analysis"))
    multi_level_data = to_dict(result.get("multi_level_framework")) or to_dict(result.get("multi_level_analysis"))

    responsible_overall = to_dict(responsible_data.get("overall"))
    try:
        responsible_score = float(responsible_overall.get("responsible_metrics_score", 0) or 0)
    except Exception:
        responsible_score = 0.0

    responsible_rating = responsible_overall.get("rating", "Standard Evaluation")

    try:
        compliance_score = float(principle_data.get("compliance_score", 0) or 0)
    except Exception:
        compliance_score = 0.0

    novelty_level = gap_data.get("novelty_level", "Unknown")
    nov_pct = gap_data.get("novelty_percentage")
    novelty_display = f"{novelty_level} ({nov_pct:.1f}%)" if nov_pct is not None else str(novelty_level)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Responsible Metrics Score", f"{responsible_score:.2f}%")
        st.caption(responsible_rating)

    with col2:
        st.metric("Principle Compliance", f"{compliance_score:.2f}%")

    with col3:
        st.metric("Novelty Level", novelty_display)
        if gap_data.get("novelty_category"):
            st.caption(gap_data.get("novelty_category"))

    # --------------------------------
    # SCORE CHART
    # --------------------------------

    chart_data = pd.DataFrame({
        "Metric": ["Responsible Metrics", "Principle Compliance"],
        "Score": [responsible_score, compliance_score]
    })

    fig = px.bar(
        chart_data,
        x="Metric",
        y="Score",
        text="Score",
        range_y=[0, 100],
        title="Research Evaluation Scores"
    )

    st.plotly_chart(fig, use_container_width=True)

    # --------------------------------
    # TABS
    # --------------------------------

    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🧠 NLP Analysis",
        "📊 Bibliometrics",
        "⚖️ Responsible Metrics",
        "🔍 Principles",
        "🧬 Research Gap",
        "🏗️ Multi-Level Framework"
    ])

    # ==================================
    # TAB 1: NLP ANALYSIS
    # ==================================

    with tab1:
        st.subheader("🧠 Key Scientific Concepts & Findings (KeyBERT)")

        # Keywords
        keywords = nlp_data.get("keywords", [])
        if keywords and isinstance(keywords, list):
            cols = st.columns(3)
            for i, item in enumerate(keywords):
                with cols[i % 3]:
                    if isinstance(item, dict):
                        kw_name = item.get("keyword") or item.get("text") or item.get("name") or str(item)
                        sc = item.get("score")
                        score_label = f" • Relevance: {float(sc):.2f}" if sc is not None else ""
                        st.info(f"**{kw_name}**{score_label}")
                    else:
                        st.info(f"**{item}**")
        else:
            st.info("No keyphrases detected.")

        st.write("")

        # Research Problem
        st.markdown("### 🎯 Research Problem Statement")
        research_problem = nlp_data.get("research_problem", [])
        if isinstance(research_problem, str):
            research_problem = [research_problem] if research_problem.strip() else []

        if isinstance(research_problem, list) and research_problem:
            with st.container(border=True):
                for problem in research_problem:
                    st.markdown(f"• {problem}")
        else:
            st.info("No research problem statement detected.")

        # Methodology
        st.markdown("### ⚙️ Academic Methodology")
        methodology = nlp_data.get("methodology", [])
        if isinstance(methodology, str):
            methodology = [methodology] if methodology.strip() else []

        if isinstance(methodology, list) and methodology:
            with st.container(border=True):
                for method in methodology:
                    st.markdown(f"• {method}")
        else:
            st.info("No methodology section detected.")

        # Contributions
        st.markdown("### 💡 Key Research Contributions")
        contributions = nlp_data.get("contributions") or nlp_data.get("research_contributions") or []
        if isinstance(contributions, str):
            contributions = [contributions] if contributions.strip() else []

        if isinstance(contributions, list) and contributions:
            with st.container(border=True):
                for contribution in contributions:
                    st.markdown(f"• {contribution}")
        else:
            st.info("No explicit contributions section detected.")

        # Findings
        st.markdown("### 📊 Key Findings & Results")
        findings = nlp_data.get("key_findings", [])
        if isinstance(findings, str):
            findings = [findings] if findings.strip() else []

        if isinstance(findings, list) and findings:
            with st.container(border=True):
                for finding in findings:
                    st.markdown(f"• {finding}")
        else:
            st.info("No key findings detected.")

    # ==================================
    # TAB 2: BIBLIOMETRICS
    # ==================================

    with tab2:
        st.subheader("📊 Bibliometric Profile & Citation Records")

        has_live_records = bool(
            isinstance(bibliometric_data, dict)
            and (
                bibliometric_data.get("citation_count") is not None
                or bibliometric_data.get("publication_year") is not None
                or bibliometric_data.get("journal")
                or bibliometric_data.get("title")
            )
        )

        if has_live_records:
            col_b1, col_b2, col_b3, col_b4 = st.columns(4)
            oa_val = bibliometric_data.get("open_access")
            if isinstance(oa_val, dict):
                oa_status = "✅ Open Access" if oa_val.get("is_oa") is True else "🔒 Closed Access"
            elif isinstance(oa_val, bool):
                oa_status = "✅ Open Access" if oa_val else "🔒 Closed Access"
            elif isinstance(oa_val, str) and oa_val.strip():
                oa_status = oa_val
            else:
                oa_status = "🔒 Closed / Unverified"

            with col_b1:
                st.metric("Total Citations", bibliometric_data.get("citation_count", 0))
            with col_b2:
                st.metric("Publication Year", bibliometric_data.get("publication_year") or "N/A")
            with col_b3:
                st.metric("Journal / Venue", str(bibliometric_data.get("journal") or "N/A")[:28])
            with col_b4:
                st.metric("Open Access", oa_status)

            with st.container(border=True):
                st.markdown("#### 📄 Verified Publication Metadata (OpenAlex API)")
                if bibliometric_data.get("title"):
                    st.write(f"**Indexed Title:** {bibliometric_data.get('title')}")
                if bibliometric_data.get("authors"):
                    authors = bibliometric_data.get("authors")
                    if isinstance(authors, list):
                        author_names = [a.get("name", str(a)) if isinstance(a, dict) else str(a) for a in authors]
                        st.write(f"**Authors:** {', '.join(author_names)}")
                    else:
                        st.write(f"**Authors:** {authors}")
                if bibliometric_data.get("doi"):
                    doi = bibliometric_data.get("doi")
                    st.markdown(f"**DOI:** [{doi}](https://doi.org/{doi})")
                if bibliometric_data.get("concepts"):
                    concepts = bibliometric_data.get("concepts", [])
                    if isinstance(concepts, list):
                        concept_names = [c.get("display_name", str(c)) if isinstance(c, dict) else str(c) for c in concepts[:6]]
                        st.write(f"**Scientific Concepts:** {', '.join(concept_names)}")
        else:
            with st.container(border=True):
                st.markdown("#### 📄 Local Bibliometric Manuscript Profile")
                st.info(
                    "ℹ️ **Local NLP Extraction Active:** This manuscript was evaluated using local text parsing. "
                    "Live OpenAlex citation counts and journal metrics are linked whenever an indexed DOI or exact title is matched in the global catalog."
                )
                col_l1, col_l2, col_l3 = st.columns(3)
                with col_l1:
                    st.metric("Pages Extracted", paper_info.get("page_count", 0))
                with col_l2:
                    st.metric("Word Count", paper_info.get("word_count", 0))
                with col_l3:
                    st.metric("Character Count", paper_info.get("character_count", 0))

    # ==================================
    # TAB 3: RESPONSIBLE METRICS
    # ==================================

    with tab3:
        st.subheader("⚖️ Responsible Metrics Evaluation")

        bonus_pts = responsible_overall.get("bibliometric_bonus", 0)

        col_r1, col_r2, col_r3 = st.columns(3)
        with col_r1:
            st.metric("Responsible Metrics Score", f"{responsible_score:.2f}%")
        with col_r2:
            st.metric("Evaluation Rating", responsible_rating)
        with col_r3:
            st.metric("Bibliometric Bonus", f"+{bonus_pts} pts")

        st.divider()

        # The 6 Assessment Dimensions
        st.markdown("### 📐 Multi-Dimensional Framework Assessment (6 Dimensions)")
        dimensions = to_dict(responsible_data.get("dimensions"))

        dim_labels = {
            "contextual_evaluation": ("Contextual Evaluation", "Considers evaluation context, tailored goals, and appropriate indicator scope."),
            "transparency": ("Transparency & Reproducibility", "Uses open, auditable methods and verifiable public citations."),
            "metric_diversity": ("Metric Diversity", "Avoids relying on a single indicator (e.g. JIF or citation count alone)."),
            "qualitative_evidence": ("Qualitative & Peer Evidence", "Integrates narrative statements, qualitative portfolio, and peer review."),
            "discipline_awareness": ("Discipline Awareness", "Accounts for field-specific differences in publication and citation speed."),
            "limitations_awareness": ("Limitations Awareness", "Explicitly warns against indicator bias, gaming, and misinterpretation.")
        }

        if dimensions:
            dim_keys = list(dimensions.keys())
            for i in range(0, len(dim_keys), 2):
                col_d1, col_d2 = st.columns(2)
                with col_d1:
                    k1 = dim_keys[i]
                    d1 = to_dict(dimensions.get(k1))
                    title1, desc1 = dim_labels.get(k1, (k1.replace("_", " ").title(), ""))
                    try:
                        score1 = float(d1.get("score", 0) or 0)
                    except Exception:
                        score1 = 0.0
                    try:
                        contrib1 = float(d1.get("weighted_contribution", 0) or 0)
                    except Exception:
                        contrib1 = 0.0
                    with st.container(border=True):
                        st.markdown(f"**{title1}**")
                        st.caption(desc1)
                        st.progress(min(1.0, max(0.0, score1 / 100.0)))
                        st.write(f"**Score:** {score1:.1f}% | **Weight:** {d1.get('weight', 0)}% | **Contribution:** {contrib1:.1f} pts")
                        kws = d1.get("matched_keywords", [])
                        if isinstance(kws, list) and kws:
                            st.write(f"*Matched concepts:* {', '.join([str(x) for x in kws[:6]])}")

                if i + 1 < len(dim_keys):
                    with col_d2:
                        k2 = dim_keys[i + 1]
                        d2 = to_dict(dimensions.get(k2))
                        title2, desc2 = dim_labels.get(k2, (k2.replace("_", " ").title(), ""))
                        try:
                            score2 = float(d2.get("score", 0) or 0)
                        except Exception:
                            score2 = 0.0
                        try:
                            contrib2 = float(d2.get("weighted_contribution", 0) or 0)
                        except Exception:
                            contrib2 = 0.0
                        with st.container(border=True):
                            st.markdown(f"**{title2}**")
                            st.caption(desc2)
                            st.progress(min(1.0, max(0.0, score2 / 100.0)))
                            st.write(f"**Score:** {score2:.1f}% | **Weight:** {d2.get('weight', 0)}% | **Contribution:** {contrib2:.1f} pts")
                            kws2 = d2.get("matched_keywords", [])
                            if isinstance(kws2, list) and kws2:
                                st.write(f"*Matched concepts:* {', '.join([str(x) for x in kws2[:6]])}")
        else:
            st.info("No responsible metrics evaluation breakdown available.")

    # ==================================
    # TAB 4: PRINCIPLES
    # ==================================

    with tab4:
        st.subheader("🔍 Leiden Manifesto & DORA Principles Compliance")
        st.metric("Compliance Score", f"{compliance_score:.2f}%")

        misuses = principle_data.get("potential_misuse", [])
        practices = principle_data.get("responsible_practices", [])
        recs = principle_data.get("recommendations", [])

        st.markdown("### ⚠️ Detected Indicator Misuses & Red Flags")
        if isinstance(misuses, list) and misuses:
            for m in misuses:
                if not isinstance(m, dict):
                    continue
                severity = str(m.get("severity", "medium")).upper()
                msg = m.get("message") or m.get("category")
                with st.container(border=True):
                    st.error(f"🚨 **[{severity}] {msg}**")
                    if m.get("explanation"):
                        st.markdown(f"**Why this is a violation:** {m['explanation']}")
                    if m.get("remediation"):
                        st.info(f"💡 **Actionable Remediation:** {m['remediation']}")
                    evidence_list = m.get("evidence", [])
                    if isinstance(evidence_list, list) and evidence_list:
                        with st.expander("🔎 View Text Evidence from Paper"):
                            for ev in evidence_list:
                                st.markdown(f"> *\"{str(ev).strip()}\"*")
        else:
            st.success("✅ **Zero Misuses Detected:** This paper does not violate DORA or Leiden Manifesto guidelines (no unadjusted cross-field comparisons or rigid journal impact factor filtering).")

        st.markdown("### ✅ Adherent Responsible Practices")
        if isinstance(practices, list) and practices:
            for pr in practices:
                if not isinstance(pr, dict):
                    continue
                category_title = str(pr.get("category", "Responsible Assessment")).replace("_", " ").title()
                with st.container(border=True):
                    st.markdown(f"**✅ {category_title}:** {pr.get('principle', '')}")
                    pr_evidence = pr.get("evidence", [])
                    if isinstance(pr_evidence, list) and pr_evidence:
                        with st.expander("🔎 View Text Evidence from Paper"):
                            for ev in pr_evidence:
                                st.markdown(f"> *\"{str(ev).strip()}\"*")
        else:
            st.info("No explicit responsible practice statements detected.")

        st.markdown("### 💡 Actionable Recommendations")
        if isinstance(recs, list) and recs:
            for i, r in enumerate(recs, 1):
                st.markdown(f"**{i}.** {r}")
        else:
            st.write("• Continue maintaining qualitative peer-review context alongside metric assessments.")

    # ==================================
    # TAB 5: RESEARCH GAP
    # ==================================

    with tab5:
        st.subheader("🧬 Potential Research Gap Detection")

        if gap_data.get("error"):
            st.warning(str(gap_data.get("error")))
        else:
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Literature Papers", gap_data.get("literature_count", 0))
            with col2:
                try:
                    sim_val = float(gap_data.get("average_similarity", 0) or 0)
                except Exception:
                    sim_val = 0.0
                st.metric("Average Similarity", f"{sim_val:.4f}")
            with col3:
                nearest_s = float(gap_data.get("nearest_similarity", 0.0) or 0.0)
                st.metric("Nearest Prior Art Match", f"{nearest_s * 100:.1f}%")
            with col4:
                nov_p = gap_data.get("novelty_percentage")
                nov_l = gap_data.get("novelty_level", "N/A")
                st.metric("Novelty Index", f"{nov_p:.1f}%" if nov_p is not None else nov_l)
                if gap_data.get("novelty_category"):
                    st.caption(gap_data.get("novelty_category"))

            st.markdown("### 🎯 Potential Gap Statement")
            st.info(gap_data.get("potential_gap", "No potential gap statement generated."))

            # Interactive 2D Scatter Plot if clustering data available
            clustering_info = to_dict(gap_data.get("clustering"))
            scatter_points = clustering_info.get("scatter_points", [])
            if isinstance(scatter_points, list) and scatter_points:
                st.markdown("### 🗺️ Thematic Literature Map (2D Embedding Projection)")
                df_points = pd.DataFrame(scatter_points)
                if "x" in df_points.columns and "y" in df_points.columns:
                    fig_map = px.scatter(
                        df_points,
                        x="x",
                        y="y",
                        color="type" if "type" in df_points.columns else None,
                        hover_name="title" if "title" in df_points.columns else None,
                        symbol="type" if "type" in df_points.columns else None,
                        title="Semantic Projection of Literature vs Uploaded Paper",
                        labels={"x": "Semantic Dimension 1 (PCA)", "y": "Semantic Dimension 2 (PCA)"}
                    )
                    fig_map.update_traces(marker=dict(size=12, line=dict(width=1, color='DarkSlateGrey')))
                    st.plotly_chart(fig_map, use_container_width=True)

            similar_papers = gap_data.get("similar_papers", [])

            # Benchmark Similarity Distribution Chart
            if isinstance(similar_papers, list) and similar_papers:
                chart_rows = []
                for p in similar_papers:
                    p_dict = to_dict(p) if isinstance(p, (dict, str)) else {}
                    t = str(p_dict.get("title", "Benchmark Paper"))[:45]
                    try:
                        sim_pct = round(float(p_dict.get("similarity", 0) or 0) * 100, 2)
                    except Exception:
                        sim_pct = 0.0
                    chart_rows.append({"Paper": t, "Similarity (%)": sim_pct})

                if chart_rows:
                    df_chart = pd.DataFrame(chart_rows).sort_values(by="Similarity (%)", ascending=True)
                    fig_sim = px.bar(
                        df_chart,
                        x="Similarity (%)",
                        y="Paper",
                        orientation="h",
                        title="Benchmark Literature Similarity Match (%)",
                        text="Similarity (%)",
                        range_x=[0, max(30, float(df_chart["Similarity (%)"].max() * 1.25))]
                    )
                    fig_sim.update_layout(yaxis_title="", xaxis_title="Similarity Score (%)")
                    st.plotly_chart(fig_sim, use_container_width=True)

            # Similar Papers Cards
            st.markdown("### 📚 Most Similar Benchmark Papers")
            if isinstance(similar_papers, list) and similar_papers:
                for idx, paper_item in enumerate(similar_papers, 1):
                    p = to_dict(paper_item) if isinstance(paper_item, (dict, str)) else {}
                    p_title = p.get("title", f"Benchmark Paper {idx}")
                    p_year = p.get("year", "N/A")
                    p_id = p.get("id", "N/A")
                    p_venue = p.get("venue", "")
                    try:
                        sim_val_num = float(p.get("similarity", 0) or 0)
                        sim_pct = sim_val_num * 100
                    except Exception:
                        sim_val_num = 0.0
                        sim_pct = 0.0

                    with st.container(border=True):
                        col_p1, col_p2 = st.columns([3, 1])
                        with col_p1:
                            st.markdown(f"**{idx}. {p_title}**")
                            meta_bits = []
                            if p_year and p_year != "N/A":
                                meta_bits.append(f"📅 Year: {p_year}")
                            if p_id and p_id != "N/A":
                                meta_bits.append(f"🆔 OpenAlex ID: {p_id}")
                            if p_venue:
                                meta_bits.append(f"🏛️ Venue: {p_venue}")
                            if meta_bits:
                                st.caption(" • ".join(meta_bits))
                        with col_p2:
                            st.metric("Similarity Match", f"{sim_pct:.2f}%")
                        st.progress(min(1.0, max(0.0, sim_val_num)))
            else:
                st.info("No benchmark literature papers matched.")

            # Underexplored Keywords Cards
            st.markdown("### 🌱 Underexplored Scientific Keywords & Themes")
            underexplored = gap_data.get("underexplored_keywords", [])
            if isinstance(underexplored, list) and underexplored:
                col_u1, col_u2 = st.columns(2)
                for idx, item in enumerate(underexplored):
                    target_col = col_u1 if idx % 2 == 0 else col_u2
                    with target_col:
                        with st.container(border=True):
                            if isinstance(item, dict):
                                kw = item.get("keyword", "Theme")
                                freq = item.get("frequency", 0)
                                st.markdown(f"🔬 **{kw}**")
                                st.caption(f"Literature Frequency: **{freq} occurrences** (High Novelty Potential)")
                            else:
                                st.markdown(f"🔬 **{item}**")
                                st.caption("High Novelty Potential")
            else:
                st.info("No underexplored keywords identified.")

    # ==================================
    # TAB 6: MULTI-LEVEL FRAMEWORK
    # ==================================

    with tab6:
        st.subheader("🏗️ Four-Level Responsible Evaluation Framework")

        try:
            ml_score = float(multi_level_data.get("overall_score", 0.0) or 0.0)
        except Exception:
            ml_score = 0.0
        ml_rating = multi_level_data.get("overall_rating", "Evaluated")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Multi-Level Overall Score", f"{ml_score:.2f}%")
        with col_m2:
            st.metric("Framework Maturity Rating", ml_rating)

        levels_data = to_dict(multi_level_data.get("levels")) or multi_level_data

        level_specs = [
            ("indicator_level", "Level 1: Indicator Level (Metric Diversity & Limits)", "Checks indicator variety, fitness for purpose, and explicit warning of metric limitations."),
            ("researcher_level", "Level 2: Researcher Level (Fairness & DORA)", "Protects individual scientists against journal-level shortcuts; emphasizes peer review and junior researchers."),
            ("institutional_level", "Level 3: Institutional Level (Field Normalization)", "Ensures comparisons across university departments normalize citation differences across fields."),
            ("system_policy_level", "Level 4: System & Policy Level (Open Data & Integrity)", "Enforces open data transparency (OpenAlex), verifiable records, and checks against citation cartels.")
        ]

        col_lvl1, col_lvl2 = st.columns(2)
        for idx, (l_key, l_title, l_desc) in enumerate(level_specs):
            l_info = to_dict(levels_data.get(l_key))
            target_col = col_lvl1 if idx % 2 == 0 else col_lvl2
            with target_col:
                with st.container(border=True):
                    st.subheader(l_title)
                    st.caption(l_desc)
                    try:
                        l_score = float(l_info.get("score", 0) or 0)
                    except Exception:
                        l_score = 0.0
                    st.progress(min(1.0, max(0.0, l_score / 100.0)))
                    st.write(f"**Score:** {l_score:.1f}% | **Rating:** {l_info.get('rating', 'Evaluated')} | **Coverage:** {l_info.get('coverage', 'N/A')}")
                    matched_kw = l_info.get("matched_keywords", [])
                    if isinstance(matched_kw, list) and matched_kw:
                        st.write(f"*Concept indicators:* {', '.join([str(x) for x in matched_kw[:6]])}")