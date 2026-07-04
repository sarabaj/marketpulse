"""
MarketPulse — Competitor Review & Sentiment Dashboard

Upload customer reviews for one or more companies (Arabic or English) and
this dashboard shows sentiment trends over time, rating distribution per
company, and (optionally, with an Anthropic API key) AI-extracted recurring
topics — exactly the kind of competitor/market analysis a Business Analyst
would compile manually from scattered reviews.

Run with: streamlit run app.py
"""
import os

import pandas as pd
import plotly.express as px
import streamlit as st

from analysis import add_sentiment_column, extract_topics_ai, top_keywords_offline

st.set_page_config(page_title="MarketPulse", page_icon="📊", layout="wide")

st.title("📊 MarketPulse")
st.caption("Turn scattered customer reviews into a competitor sentiment overview.")

# ---------- Data loading ----------
uploaded = st.sidebar.file_uploader(
    "Upload reviews CSV (company, review_text, rating, date)", type="csv"
)

if uploaded:
    df = pd.read_csv(uploaded, parse_dates=["date"])
else:
    st.sidebar.info("No file uploaded — showing sample data (3 fintech competitors).")
    df = pd.read_csv("data/reviews.csv", parse_dates=["date"])

df = add_sentiment_column(df)

companies = st.sidebar.multiselect(
    "Filter companies", options=df["company"].unique(), default=list(df["company"].unique())
)
df = df[df["company"].isin(companies)]

# ---------- KPI row ----------
col1, col2, col3 = st.columns(3)
col1.metric("Total reviews", len(df))
col2.metric("Avg. rating", f"{df['rating'].mean():.1f} / 5")
negative_pct = (df["sentiment"] == "negative").mean() * 100
col3.metric("% negative reviews", f"{negative_pct:.0f}%")

# ---------- Charts ----------
c1, c2 = st.columns(2)

with c1:
    st.subheader("Average rating by company")
    avg_by_company = df.groupby("company")["rating"].mean().reset_index()
    fig = px.bar(avg_by_company, x="company", y="rating", color="company",
                 range_y=[0, 5])
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Sentiment breakdown by company")
    sentiment_counts = df.groupby(["company", "sentiment"]).size().reset_index(name="count")
    fig2 = px.bar(sentiment_counts, x="company", y="count", color="sentiment",
                  color_discrete_map={"positive": "#2f9e44", "neutral": "#f08c00", "negative": "#e03131"},
                  barmode="stack")
    st.plotly_chart(fig2, use_container_width=True)

st.subheader("Rating trend over time")
df["month"] = pd.to_datetime(df["date"]).dt.to_period("M").astype(str)
trend = df.groupby(["month", "company"])["rating"].mean().reset_index()
fig3 = px.line(trend, x="month", y="rating", color="company", markers=True, range_y=[0, 5])
st.plotly_chart(fig3, use_container_width=True)

# ---------- Topic extraction ----------
st.subheader("🔎 Recurring themes")

has_api_key = bool(os.getenv("ANTHROPIC_API_KEY"))

if not has_api_key:
    st.info(
        "AI topic extraction needs an `ANTHROPIC_API_KEY` environment variable. "
        "Showing an offline keyword frequency fallback instead."
    )
    keywords = top_keywords_offline(df["review_text"].tolist())
    kw_df = pd.DataFrame(keywords, columns=["keyword", "mentions"])
    st.dataframe(kw_df, use_container_width=True)
else:
    if st.button("Extract topics with AI"):
        with st.spinner("Analyzing reviews with Claude…"):
            topics = extract_topics_ai(df["review_text"].tolist())
        if topics:
            st.dataframe(pd.DataFrame(topics), use_container_width=True)
        else:
            st.warning("AI extraction returned no results — check your API key or try again.")

st.subheader("Sample reviews")
st.dataframe(
    df[["company", "review_text", "rating", "sentiment", "date"]].sort_values("date", ascending=False),
    use_container_width=True,
)
