import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path

from src.rag import ask_rag


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Brand / Customer Review Insight Platform",
    layout="wide"
)

st.title("AI Brand / Customer Review Insight Platform")

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

        st.subheader("Static Visualizations")

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

        st.subheader("Interactive Visualizations")

        for html_path in html_files:

            with st.container(border=True):

                st.markdown(
                    f"### {html_path.stem.replace('_', ' ').title()}"
                )

                html_content = html_path.read_text(
                    encoding="utf-8"
                )

                components.html(
                    html_content,
                    height=800,
                    scrolling=True
                )

else:
    st.warning("No plots found for this brand.")

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