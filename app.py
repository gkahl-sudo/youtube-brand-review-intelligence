import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
from src.rag import ask_rag
from src.analytics import (
    generate_sql,
    execute_sql
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Brand / Customer Intelligence Platform (YouTube)",
    layout="wide"
)

st.title("AI Brand / Customer Intelligence Platform (YouTube)")

# =========================
# BRAND MAPPING
# =========================

brand_mapping = {
    "Zalando": "zalando_review",
    "DHL": "dhl_logistik_experiences_erfahrungen",
    "Alibaba": "alibaba_review",
    "Etsy": "etsy_experiences"
}

selected_brand = st.selectbox(
    "Choose brand",
    list(brand_mapping.keys())
)

query_slug = brand_mapping[selected_brand]

# =========================
# SUGGESTED QUESTIONS
# =========================

example_questions = {
    "Zalando":
        "What are the main complaints and pain points for Zalando customers? What are popular views held about the platform and is there feedback for improvement?",

    "DHL":
        "What are the main complaints and pain points for customers of DHL? What is said about working conditions at DHL?",

    "Alibaba":
        "What are the main complaints and pain points for customers of Alibaba?",

    "Etsy":
        "What are the main complaints and pain points for sellers and buyers on Etsy? What are popular views held about the platform?"
}

st.info(
    f"Suggested question:\n\n{example_questions[selected_brand]}"
)

st.divider()

# =========================
# DASHBOARD
# =========================

st.header("Analytics Dashboard")

PROJECT_ROOT = Path(__file__).resolve().parent

plots_path = PROJECT_ROOT / "plots" / selected_brand

html_files = []
image_files = []

if plots_path.exists():

    image_files = sorted(
        list(plots_path.glob("*.png"))
        + list(plots_path.glob("*.jpg"))
        + list(plots_path.glob("*.jpeg"))
    )

    html_files = sorted(
        list(plots_path.glob("*.html"))
    )

    # =========================
    # STATIC IMAGE GRID
    # =========================

    if image_files:

        st.subheader("Video Stats & KPIs (Static)")

        cols = st.columns(2)

        for idx, image_path in enumerate(image_files):

            with cols[idx % 2]:

                with st.container(border=True):

                    st.image(
                        str(image_path),
                        use_container_width=True
                    )

                    st.caption(
                        image_path.stem
                        .replace("_", " ")
                        .title()
                    )

# =========================
# INTERACTIVE PLOTLY
# =========================

if html_files:

    st.subheader("Visualizations (Interactive)")

    # -------------------------
    # Locate expected plots
    # -------------------------

    semantic_map = None
    semantic_clusters = None
    dar_cts_map = None
    remaining_plots = []

    for html_path in html_files:

        stem = html_path.stem.lower()

        if stem == "semantic_map":
            semantic_map = html_path

        elif stem == "semantic_clusters":
            semantic_clusters = html_path

        elif stem == "dar_cts_quadrant_map":
            dar_cts_map = html_path

        else:
            remaining_plots.append(html_path)

    # -------------------------
    # ROW 1
    # Semantic visualizations
    # -------------------------

    col1, col2 = st.columns(2)

    if semantic_map:

        with col1:

            with st.container(border=True):

                st.markdown("### Semantic Map")

                html_content = semantic_map.read_text(
                    encoding="utf-8"
                )

                components.html(
                    html_content,
                    height=650,
                    scrolling=True
                )

    if semantic_clusters:

        with col2:

            with st.container(border=True):

                st.markdown("### Semantic Clusters")

                html_content = semantic_clusters.read_text(
                    encoding="utf-8"
                )

                components.html(
                    html_content,
                    height=650,
                    scrolling=True
                )

    # -------------------------
    # ROW 2
    # DAR CTS Quadrant Map
    # -------------------------

    if dar_cts_map:

        st.markdown("### DAR CTS Quadrant Map")

        with st.container(border=True):

            html_content = dar_cts_map.read_text(
                encoding="utf-8"
            )

            components.html(
                html_content,
                height=700,
                scrolling=True
            )

    # -------------------------
    # Any additional plots
    # -------------------------

    if remaining_plots:

        st.subheader("Additional Visualizations")

        cols = st.columns(3)

        for idx, html_path in enumerate(remaining_plots):

            with cols[idx % 3]:

                with st.container(border=True):

                    title = (
                        html_path.stem
                        .replace("_", " ")
                        .title()
                    )

                    st.markdown(f"### {title}")

                    html_content = html_path.read_text(
                        encoding="utf-8"
                    )

                    components.html(
                        html_content,
                        height=650,
                        scrolling=True
                    )

else:

    st.warning(
        "No plots found for this brand."
    )

# =========================

# ANALYTICS EXPLORER

# =========================

st.divider()

st.header("Analytics Explorer")

suggested_analytics = [
    "Top customer complaints",
    "Most negative comments",
    "Most positive comments",
    "Sentiment distribution",
    "Compare sentiment by video type",
    "Most common discussion topics",
    "Comments mentioning delivery",
    "Comments mentioning price"
]

selected_template = st.selectbox(
    "Suggested analytics requests",
    ["Custom request"] + suggested_analytics
)

default_request = (
    selected_template
    if selected_template != "Custom request"
    else ""
)

analytics_request = st.text_area(
    "Describe the analysis you want",
    value=default_request,
    height=100
)

if st.button("Run Analytics"):

    if analytics_request.strip():

        with st.spinner("Generating analysis query..."):

            try:

                sql = generate_sql(
                    user_request=analytics_request,
                    brand_name=selected_brand,
                    query_slug=query_slug
                )

                df = execute_sql(sql)

                st.subheader("Results")

                st.dataframe(
                    df,
                    use_container_width=True
                )

                # =========================
                # AUTO VISUALIZATION
                # =========================

                numeric_cols = df.select_dtypes(
                    include=["number"]
                ).columns

                if (
                    len(df.columns) == 2
                    and len(numeric_cols) == 1
                ):

                    st.subheader("Visualization")

                    chart_df = df.set_index(
                        df.columns[0]
                    )

                    st.bar_chart(chart_df)

                # =========================
                # SQL TRANSPARENCY
                # =========================

                with st.expander(
                    "Generated SQL"
                ):
                    st.code(
                        sql,
                        language="sql"
                    )

            except Exception as e:

                st.error(
                    f"Analytics query failed: {e}"
                )


# =========================
# CHATBOT
# =========================

st.header("Customer Intelligence Chatbot")

user_question = st.text_area(
    "Ask a question about customer opinions",
    value=example_questions[selected_brand],
    height=120
)

if st.button("Analyze"):

    if user_question.strip():

        with st.spinner("Analyzing customer feedback..."):

            answer, top_comments = ask_rag(
                question=user_question,
                query_slug=query_slug
            )

        # =========================
        # AI RESPONSE
        # =========================

        st.subheader("AI Analysis")

        st.write(answer)

        # =========================
        # RETRIEVED COMMENTS
        # =========================

        with st.expander("Retrieved Comments"):

            st.dataframe(
                top_comments[
                    [
                        "text",
                        "sentiment",
                        "video_type",
                        "similarity"
                    ]
                ]
            )