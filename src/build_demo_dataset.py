import pandas as pd
import sqlite3
from pathlib import Path

# --- project root (go up from src/) ---
PROJECT_ROOT = Path(__file__).resolve().parents[1]

# --- input DB ---
db_path = PROJECT_ROOT / "database" / "youtube_reviews.db"

conn = sqlite3.connect(db_path)

# --- output DB ---
demo_db_path = PROJECT_ROOT / "demobase" / "youtube_demo.db"
demo_db_path.parent.mkdir(parents=True, exist_ok=True)

# =========================
# LOAD DATA
# =========================

videos = pd.read_sql("SELECT * FROM videos", conn)

demo_videos = (
    videos
    .groupby("query_slug", group_keys=False)
    .apply(
        lambda x: x.sample(
            n=min(50, len(x)),
            random_state=42
        )
))

comments = pd.read_sql("SELECT * FROM comments", conn)

demo_comments = comments[
    comments["video_id"].isin(demo_videos["video_id"])
]

demo_comments = (
    demo_comments
    .groupby("video_id", group_keys=False)
    .apply(
        lambda x: x.sample(
            n=min(20, len(x)),
            random_state=42
        )
    )
)

comment_embeddings = pd.read_sql(
    "SELECT * FROM comment_embeddings",
    conn
)

demo_embeddings = comment_embeddings[
    comment_embeddings["comment_id"].isin(demo_comments["comment_id"])
]

# =========================
# SAVE DEMO DB
# =========================

demo_conn = sqlite3.connect(demo_db_path)

demo_videos.to_sql("videos", demo_conn, index=False, if_exists="replace")
demo_comments.to_sql("comments", demo_conn, index=False, if_exists="replace")
demo_embeddings.to_sql("comment_embeddings", demo_conn, index=False, if_exists="replace")

demo_conn.close()
conn.close()