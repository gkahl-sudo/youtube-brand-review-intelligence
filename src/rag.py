import json
import numpy as np
import pandas as pd

from openai import OpenAI
from sklearn.metrics.pairwise import cosine_similarity

from src.database import get_connection


import streamlit as st

client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"]
)

SYSTEM_PROMPT = """
You are a customer intelligence analyst.

Answer questions based ONLY on the retrieved YouTube comments and metadata.

Summarize recurring themes and mention sentiment patterns.

Identify:
- recurring complaints
- customer sentiment
- product/service issues
- positive feedback patterns

Do not invent information.
"""


def ask_rag(question, query_slug, top_k=10):

    conn = get_connection()

    # =========================
    # Embed user question
    # =========================

    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=question
    )

    question_embedding = response.data[0].embedding

    # =========================
    # Load comments + embeddings
    # =========================

    comments_rag = pd.read_sql(
        """
        SELECT
            c.comment_id,
            c.text,
            c.sentiment,
            c.video_type,

            e.embedding_json

        FROM comments c

        LEFT JOIN comment_embeddings e
            ON c.comment_id = e.comment_id
            AND c.query_slug = e.query_slug

        WHERE c.query_slug = ?
        """,
        conn,
        params=[query_slug]
    )

    conn.close()

    # =========================
    # Convert embeddings
    # =========================

    comments_rag["embedding"] = (
        comments_rag["embedding_json"]
        .apply(json.loads)
    )

    embedding_matrix = np.vstack(
        comments_rag["embedding"]
    )

    # =========================
    # Similarity search
    # =========================

    similarities = cosine_similarity(
        [question_embedding],
        embedding_matrix
    )[0]

    comments_rag["similarity"] = similarities

    top_comments = (
        comments_rag
        .sort_values(
            "similarity",
            ascending=False
        )
        .head(top_k)
    )

    # =========================
    # Build context
    # =========================

    context = "\n\n".join(
        top_comments["text"].tolist()
    )

    # =========================
    # LLM answer
    # =========================

    chat_response = client.chat.completions.create(
        model="gpt-4o-mini",

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },

            {
                "role": "user",
                "content":
                f"""
                USER QUESTION:
                {question}

                COMMENTS:
                {context}
                """
            }
        ]
    )

    answer = chat_response.choices[0].message.content

    return answer, top_comments