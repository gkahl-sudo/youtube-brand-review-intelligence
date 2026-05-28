import streamlit as st

st.title("AI Customer Insight Platform")

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

st.write(f"You selected: {selected_brand}")
st.write(f"Query slug: {query_slug}")