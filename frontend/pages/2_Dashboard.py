import streamlit as st
import pandas as pd
import plotly.express as px

from utils.api import get_analysis_history


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(

    page_title="Dashboard | ResponsibleMetrics AI",

    page_icon="📊",

    layout="wide"
)


# ==========================================
# PAGE TITLE
# ==========================================

st.title("📊 Research Analytics Dashboard")

st.write(
    """
    Overview of all research papers analyzed
    using the ResponsibleMetrics AI framework.
    """
)

st.divider()


# ==========================================
# LOAD DATA
# ==========================================

with st.spinner("Loading analysis data..."):

    response = get_analysis_history()


# ==========================================
# ERROR HANDLING
# ==========================================

if "error" in response:

    st.error(
        "Unable to load analysis history."
    )

    st.code(
        response["error"]
    )

    st.stop()


# ==========================================
# EXTRACT PAPERS
# ==========================================

papers = response.get(
    "papers",
    []
)


if not papers:

    st.info(
        """
        No research papers have been analyzed yet.

        Go to the Analyze Paper page to upload
        and analyze your first research paper.
        """
    )

    st.stop()


# ==========================================
# CREATE DATAFRAME
# ==========================================

df = pd.DataFrame(
    papers
)


# ==========================================
# CLEAN NUMERIC DATA
# ==========================================

numeric_columns = [

    "responsible_score",

    "compliance_score",

    "average_similarity"
]


for column in numeric_columns:

    if column in df.columns:

        df[column] = pd.to_numeric(

            df[column],

            errors="coerce"
        )


# ==========================================
# CALCULATE METRICS
# ==========================================

total_papers = len(df)


average_responsible_score = round(

    df["responsible_score"].mean()

    if "responsible_score" in df.columns

    else 0,

    2
)


average_compliance_score = round(

    df["compliance_score"].mean()

    if "compliance_score" in df.columns

    else 0,

    2
)


average_similarity = round(

    df["average_similarity"].mean()

    if "average_similarity" in df.columns

    else 0,

    2
)


# ==========================================
# TOP METRICS
# ==========================================

st.subheader("📌 Overall Statistics")


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(

        "Papers Analyzed",

        total_papers
    )


with col2:

    st.metric(

        "Avg Responsible Score",

        f"{average_responsible_score}%"
    )


with col3:

    st.metric(

        "Avg Compliance Score",

        f"{average_compliance_score}%"
    )


with col4:

    st.metric(

        "Avg Literature Similarity",

        average_similarity
    )


st.divider()


# ==========================================
# SCORE COMPARISON
# ==========================================

st.subheader(
    "📊 Paper Score Comparison"
)


if (

    "responsible_score" in df.columns

    and

    "compliance_score" in df.columns

):

    chart_df = df.copy()


    if "title" not in chart_df.columns:

        chart_df["title"] = (

            "Paper " +

            chart_df.index.astype(str)
        )


    chart_df["title"] = (

        chart_df["title"]
        .fillna("Unknown Paper")
        .astype(str)
        .str[:40]
    )


    melted_df = chart_df.melt(

        id_vars=["title"],

        value_vars=[

            "responsible_score",

            "compliance_score"
        ],

        var_name="Metric",

        value_name="Score"
    )


    fig_scores = px.bar(

        melted_df,

        x="title",

        y="Score",

        color="Metric",

        barmode="group",

        range_y=[0, 100],

        title="Responsible Metrics vs Principle Compliance"
    )


    fig_scores.update_layout(

        xaxis_title="Research Paper",

        yaxis_title="Score (%)",

        legend_title="Metric"
    )


    st.plotly_chart(

        fig_scores,

        use_container_width=True
    )


# ==========================================
# TWO COLUMN ANALYTICS
# ==========================================

col1, col2 = st.columns(2)


# ==========================================
# NOVELTY DISTRIBUTION
# ==========================================

with col1:

    st.subheader(
        "🧬 Novelty Distribution"
    )


    if (

        "novelty_level" in df.columns

        and

        not df["novelty_level"].dropna().empty

    ):


        novelty_counts = (

            df["novelty_level"]

            .fillna("Unknown")

            .value_counts()

            .reset_index()
        )


        novelty_counts.columns = [

            "Novelty Level",

            "Count"
        ]


        fig_novelty = px.pie(

            novelty_counts,

            names="Novelty Level",

            values="Count",

            title="Research Novelty Levels"
        )


        st.plotly_chart(

            fig_novelty,

            use_container_width=True
        )


    else:

        st.info(
            "No novelty data available."
        )


# ==========================================
# SCORE DISTRIBUTION
# ==========================================

with col2:

    st.subheader(
        "📈 Responsible Score Distribution"
    )


    if "responsible_score" in df.columns:


        fig_distribution = px.histogram(

            df,

            x="responsible_score",

            nbins=10,

            title="Distribution of Responsible Metrics Scores"
        )


        fig_distribution.update_layout(

            xaxis_title="Score",

            yaxis_title="Number of Papers"
        )


        st.plotly_chart(

            fig_distribution,

            use_container_width=True
        )


    else:

        st.info(
            "No responsible score data available."
        )


st.divider()


# ==========================================
# RECENT PAPERS
# ==========================================

st.subheader(
    "📄 Recent Paper Analyses"
)


display_columns = [

    "id",

    "title",

    "filename",

    "responsible_score",

    "compliance_score",

    "novelty_level"
]


available_columns = [

    column

    for column in display_columns

    if column in df.columns
]


recent_df = df[

    available_columns

].copy()


# Rename columns

rename_map = {

    "id": "ID",

    "title": "Paper Title",

    "filename": "Filename",

    "responsible_score": "Responsible Score",

    "compliance_score": "Compliance Score",

    "novelty_level": "Novelty"
}


recent_df.rename(

    columns=rename_map,

    inplace=True
)


st.dataframe(
    recent_df,
    use_container_width=True,
    hide_index=True
)

# Row Action: View selected row in Analysis Report
col_view_sel, col_view_btn = st.columns([3, 1])
with col_view_sel:
    dash_paper_options = {
        f"ID {p['id']} - {p.get('title') or p.get('filename')}": p["id"]
        for p in papers
    }
    selected_dash_label = st.selectbox(
        "Select a paper row to inspect:",
        list(dash_paper_options.keys()),
        key="dash_select_row"
    )
with col_view_btn:
    st.write("")
    st.write("")
    if st.button("👁 View in Analysis Report", use_container_width=True):
        st.session_state["selected_paper_id"] = dash_paper_options[selected_dash_label]
        st.switch_page("pages/4_Analysis_Report.py")