import streamlit as st

from src.rag import ask_rag


st.set_page_config(
    page_title="AI Customer Insight Platform",
    layout="wide"
)

st.title("AI Customer Insight Platform")

# =========================
# Brand selector
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

st.divider()

# =========================
# Chat interface
# =========================

user_question = st.text_input(
    "Ask a question about customer opinions"
)

if st.button("Analyze"):

    if user_question.strip():

        with st.spinner("Analyzing customer feedback..."):

            answer, top_comments = ask_rag(
                question=user_question,
                query_slug=query_slug
            )

        # =========================
        # LLM answer
        # =========================

        st.subheader("AI Analysis")

        st.write(answer)

        # =========================
        # Retrieved comments
        # =========================

        st.subheader("Retrieved Comments")

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