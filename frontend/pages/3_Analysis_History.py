import streamlit as st
import pandas as pd

from utils.api import (
    get_history,
    get_paper_analysis,
    delete_paper
)


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(

    page_title="Analysis History | ResponsibleMetrics AI",

    page_icon="📚",

    layout="wide"
)


# ==========================================
# PAGE TITLE
# ==========================================

st.title("📚 Analysis History")

st.write(
    """
    View and manage previously analyzed research papers.
    """
)

st.divider()


# ==========================================
# LOAD HISTORY
# ==========================================

with st.spinner("Loading analysis history..."):

    response = get_history()


# ==========================================
# ERROR HANDLING
# ==========================================

if not response:

    st.error(
        "Unable to connect to the backend."
    )

    st.stop()


if "error" in response:

    st.error(
        "Unable to load analysis history."
    )

    st.code(
        response["error"]
    )

    st.stop()


# ==========================================
# GET PAPERS
# ==========================================

papers = response.get(
    "papers",
    []
)


if not papers:

    st.info(
        """
        No research paper analyses found.

        Go to the Analyze Paper page to analyze
        your first research paper.
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
# SEARCH AND FILTER SECTION
# ==========================================

st.subheader("🔎 Search & Filter")


col1, col2, col3 = st.columns(3)


# ------------------------------------------
# SEARCH
# ------------------------------------------

with col1:

    search_query = st.text_input(

        "Search Paper",

        placeholder="Search by title or filename..."
    )


# ------------------------------------------
# NOVELTY FILTER
# ------------------------------------------

with col2:

    novelty_options = ["All"]


    if "novelty_level" in df.columns:

        novelty_values = (

            df["novelty_level"]

            .dropna()

            .unique()

            .tolist()
        )


        novelty_options.extend(

            sorted(novelty_values)
        )


    novelty_filter = st.selectbox(

        "Novelty Level",

        novelty_options
    )


# ------------------------------------------
# SCORE FILTER
# ------------------------------------------

with col3:

    score_filter = st.selectbox(

        "Responsible Score",

        [

            "All",

            "0 - 25%",

            "26 - 50%",

            "51 - 75%",

            "76 - 100%"
        ]
    )


# ==========================================
# APPLY SEARCH FILTER
# ==========================================

filtered_df = df.copy()


if search_query:

    search_query = search_query.lower()


    filtered_df = filtered_df[

        filtered_df["title"]

        .fillna("")

        .str.lower()

        .str.contains(search_query)

        |

        filtered_df["filename"]

        .fillna("")

        .str.lower()

        .str.contains(search_query)

    ]


# ==========================================
# APPLY NOVELTY FILTER
# ==========================================

if novelty_filter != "All":

    filtered_df = filtered_df[

        filtered_df["novelty_level"]

        == novelty_filter

    ]


# ==========================================
# APPLY SCORE FILTER
# ==========================================

if "responsible_score" in filtered_df.columns:

    filtered_df["responsible_score"] = pd.to_numeric(

        filtered_df["responsible_score"],

        errors="coerce"
    )


if score_filter == "0 - 25%":

    filtered_df = filtered_df[

        filtered_df["responsible_score"]

        .between(0, 25)
    ]


elif score_filter == "26 - 50%":

    filtered_df = filtered_df[

        filtered_df["responsible_score"]

        .between(26, 50)
    ]


elif score_filter == "51 - 75%":

    filtered_df = filtered_df[

        filtered_df["responsible_score"]

        .between(51, 75)
    ]


elif score_filter == "76 - 100%":

    filtered_df = filtered_df[

        filtered_df["responsible_score"]

        .between(76, 100)
    ]


# ==========================================
# RESULTS COUNT
# ==========================================

st.caption(

    f"Showing {len(filtered_df)} of {len(df)} analyzed papers"
)


st.divider()


# ==========================================
# DISPLAY PAPERS
# ==========================================

if filtered_df.empty:

    st.warning(
        "No papers match the selected filters."
    )


else:

    for _, paper in filtered_df.iterrows():

        paper_id = paper.get("id")


        title = paper.get(

            "title",

            "Unknown Title"
        )


        filename = paper.get(

            "filename",

            "Unknown File"
        )


        responsible_score = paper.get(

            "responsible_score",

            0
        )


        compliance_score = paper.get(

            "compliance_score",

            0
        )


        novelty_level = paper.get(

            "novelty_level",

            "Unknown"
        )


        responsible_rating = paper.get(

            "responsible_rating",

            "Unknown"
        )


        created_at = paper.get(

            "created_at",

            "Unknown"
        )


        # ==================================
        # PAPER CARD
        # ==================================

        with st.container(

            border=True
        ):


            st.subheader(

                f"📄 {title}"
            )


            st.caption(

                f"File: {filename}"
            )


            # ------------------------------
            # METRICS
            # ------------------------------

            metric_col1, metric_col2, metric_col3, metric_col4 = (

                st.columns(4)

            )


            with metric_col1:

                st.metric(

                    "Responsible Score",

                    f"{responsible_score}%"
                )


            with metric_col2:

                st.metric(

                    "Compliance Score",

                    f"{compliance_score}%"
                )


            with metric_col3:

                st.metric(

                    "Novelty",

                    novelty_level
                )


            with metric_col4:

                st.metric(

                    "Rating",

                    responsible_rating
                )


            # ------------------------------
            # DATE
            # ------------------------------

            st.caption(

                f"Analyzed: {created_at}"
            )


            # ------------------------------
            # ACTION BUTTONS
            # ------------------------------

            button_col1, button_col2, button_col3 = (

                st.columns(

                    [2, 2, 6]
                )

            )


            # ==============================
            # VIEW DETAILS
            # ==============================

            with button_col1:

                view_button = st.button(

                    "👁 View Analysis",

                    key=f"view_{paper_id}"
                )


            # ==============================
            # DELETE
            # ==============================

            with button_col2:

                delete_button = st.button(

                    "🗑 Delete",

                    key=f"delete_{paper_id}"
                )


            # ==============================
            # VIEW ANALYSIS
            # ==============================

            if view_button:

                st.session_state[
                    "selected_paper_id"
                ] = paper_id


                st.switch_page(
                    "pages/4_Analysis_Report.py"
                )


            # ==============================
            # DELETE ANALYSIS
            # ==============================

            if delete_button:

                with st.spinner(

                    "Deleting analysis..."
                ):

                    delete_response = (

                        delete_paper(
                            paper_id
                        )
                    )


                if "error" in delete_response:

                    st.error(

                        delete_response[
                            "error"
                        ]
                    )


                else:

                    st.success(

                        "Analysis deleted successfully!"
                    )


                    st.rerun()


# ==========================================
# TABLE VIEW
# ==========================================

st.divider()

st.subheader("📊 Table View")


table_columns = [

    "id",

    "title",

    "filename",

    "responsible_score",

    "compliance_score",

    "novelty_level",

    "created_at"
]


available_columns = [

    column

    for column in table_columns

    if column in filtered_df.columns
]


table_df = filtered_df[

    available_columns

].copy()


table_df.rename(

    columns={

        "id": "ID",

        "title": "Paper Title",

        "filename": "Filename",

        "responsible_score": "Responsible Score",

        "compliance_score": "Compliance Score",

        "novelty_level": "Novelty",

        "created_at": "Analysis Date"
    },

    inplace=True
)


st.dataframe(

    table_df,

    use_container_width=True,

    hide_index=True
)

col_hist_csv, _ = st.columns([1.5, 3.5])
with col_hist_csv:
    csv_history = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Export Table to CSV",
        data=csv_history,
        file_name="ResponsibleMetrics_Analysis_History.csv",
        mime="text/csv",
        use_container_width=True
    )