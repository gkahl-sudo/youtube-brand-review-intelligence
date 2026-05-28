import streamlit as st

from pathlib import Path

from src.rag import ask_rag


# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Customer Insight Platform",
    layout="wide"
)

st.title("AI Customer Insight Platform")

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
# DISPLAY PLOTS
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

    for image_path in image_files:

        st.image(
            str(image_path),
            caption=image_path.stem,
            use_container_width=True
        )

else:
    st.warning("No plots found for this brand.")

st.divider()

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