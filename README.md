# AI Brand / Customer Intelligence Platform (YouTube)

## Overview

This project explores how Large Language Models (LLMs), semantic embeddings, and modern NLP pipelines can be combined to generate actionable customer intelligence from large-scale YouTube discussions.

The platform retrieves videos and comments related to major e-commerce and logistics brands, enriches the data using semantic and statistical methods, stores the processed information in a SQLite data warehouse, and exposes the results through an interactive Streamlit dashboard with Retrieval-Augmented Generation (RAG).

Brands analyzed:

* Zalando
* DHL
* Alibaba
* Etsy

The project combines:

* Data Engineering
* NLP / Semantic Embedding
* Exploratory Data Analysis
* Clustering & Dimensionality Reduction
* Retrieval-Augmented Generation (RAG)
* Interactive Dashboarding

A Demo Version can be found on Streamlit:
https://youtube-brand-review-intelligence-v5czl6rnbmborywaqvpoyg.streamlit.app/

---

# Project Architecture

YouTube API
→ preprocessing & semantic enrichment
→ SQLite data warehouse
→ embedding generation
→ semantic clustering & analytics
→ Streamlit dashboard + RAG chatbot

---

# Notebook 01 — YouTube Data Retrieval

## Goal

Retrieve large-scale YouTube data related to brand perception and customer discussions.

## Functionality

* Connection to the YouTube Data API
* Retrieval of:

  * video metadata
  * top-level comments
* Query-specific storage structure
* Automatic handling of videos with disabled comments
* Persistent raw-data storage as `.csv`

## Data Retrieved

Per brand:

* ~100 YouTube videos
* Up to ~100 comments per video

Resulting in:

* several thousand semantically rich customer comments

---

# Notebook 02 — Semantic Preprocessing & Exploratory Data Analysis

## Goal

Clean, enrich, and analyze textual customer discussions.

## Preprocessing Steps

* Text cleaning
* Missing-value handling
* Timestamp processing
* Language detection
* Sentiment analysis

## Semantic Enrichment

Additional engineered variables include:

* `clean_text`
* `sentiment`
* `language`
* `log_like_count`
* `log_comment_count`

## Custom Marketing KPIs

### Discussion Activation Rate (DAR)

Measures how strongly a video activates discussion relative to engagement.

### Controversy Tension Score (CTS)

Measures emotional tension / polarization within discussions.

These KPIs were designed to capture online discourse dynamics beyond simple sentiment analysis.

## Exploratory Analyses

* Sentiment distributions
* Language distributions
* Comment activity over time
* Like ↔ comment correlations
* DAR / CTS analytics
* Video engagement patterns

---

# Notebook 03 — SQLite Data Warehouse & Semantic Embeddings

## Goal

Create a structured semantic data warehouse for downstream analytics and retrieval.

## SQLite Data Warehouse

Implemented tables:

* `videos`
* `comments`
* `comment_embeddings`
* `video_title_embeddings`
* `video_description_embeddings`

## Additional Feature Engineering

* `video_type` classification

  * review
  * news
  * other

* SQL-based aggregation analyses

* Duplicate-handling logic

* Query-aware storage architecture

## Semantic Embeddings

OpenAI embeddings (`text-embedding-3-small`) were generated for:

* comments
* video titles
* video descriptions

Embeddings were stored separately from raw tables for scalability and modularity.

---

# Notebook 04 — Semantic Clustering & Retrieval-Augmented Generation

## Goal

Transform customer discussions into an interactive semantic intelligence system.

## Semantic Mapping

Implemented:

* UMAP dimensionality reduction
* 2D and 3D semantic visualization

## Clustering

HDBSCAN was used to identify semantically coherent discussion clusters such as:

* shipping complaints
* scam accusations
* positive product reviews
* platform trust issues

## DAR / CTS Landscape Analysis

Custom interactive visualizations were developed to analyze:

* engagement intensity
* controversy dynamics
* discourse activation patterns

## Retrieval-Augmented Generation (RAG)

A semantic retrieval pipeline was implemented using:

* OpenAI embeddings
* cosine similarity search
* GPT-4o-mini

The chatbot:

1. embeds the user query
2. retrieves semantically similar comments
3. generates evidence-based customer insight summaries

Example queries:

* “What are common complaints about DHL?”
* “What feedback exists from Zalando customers?”
* “What are recurring trust concerns about Alibaba?”

---

# Streamlit Web Application

An interactive Streamlit dashboard was developed featuring:

* brand selection
* semantic visualizations
* KPI dashboards
* interactive Plotly analytics
* AI-powered customer insight chatbot

The application integrates:

* SQLite
* Plotly
* OpenAI API
* semantic retrieval
* Retrieval-Augmented Generation

---

# Technologies Used

## Data & Analytics

* Python
* Pandas
* NumPy
* SQLite

## NLP & AI

* OpenAI API
* VaderSentiment
* LangDetect

## Machine Learning

* UMAP
* HDBSCAN
* Scikit-learn

## Visualization

* Plotly
* Matplotlib
* Seaborn
* Streamlit

## APIs

* YouTube Data API v3

---

# Key Learnings

This project demonstrates how modern NLP pipelines and LLM-based retrieval systems can be combined to:

* structure unstructured customer discussions
* identify recurring pain points
* visualize semantic discourse landscapes
* support scalable customer intelligence workflows

It further illustrates how semantic embeddings and RAG architectures can bridge traditional analytics and conversational AI systems.

---

# Future Extensions

Potential future improvements include:

* multi-platform integration (Reddit, TikTok, X)
* real-time monitoring pipelines
* vector databases (FAISS / Pinecone)
* fine-tuned industry-specific models
* automated trend and anomaly detection
* multilingual semantic analysis
