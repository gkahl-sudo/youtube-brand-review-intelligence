# Analytics file for SQL queries
import pandas as pd

from openai import OpenAI

from src.database import get_connection

client = OpenAI()

def generate_sql(
user_request: str,
brand_name: str,
query_slug: str
):

    schema = """
    Table comments(
        id,
        text,
        sentiment,
        video_type,
        similarity,
        created_at,
        query_slug
    )
    """

    prompt = f"""

    You are an expert SQLite analyst.

    Database schema:

    {schema}

    The user is currently analyzing the brand:

    {brand_name}

    Important:

    * The database identifies this brand using:
    query_slug = '{query_slug}'
    * Always filter results to this query_slug.
    * Never ask the user about query_slug.
    * Only generate a SQLite SELECT statement.
    * Never generate INSERT, UPDATE, DELETE, DROP, ALTER, or CREATE statements.
    * Limit non-aggregated queries to 100 rows.
    * Return SQL only.
    * Do not use markdown.
    * Do not provide explanations.

    User request:
    {user_request}
    """


    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    sql = response.choices[0].message.content.strip()

    if not sql.lower().startswith("select"):
        raise ValueError(
            "Only SELECT statements are allowed."
        )

    return sql


def execute_sql(sql: str):


conn = get_connection()

try:
    return pd.read_sql_query(
        sql,
        conn
    )

finally:
    conn.close()