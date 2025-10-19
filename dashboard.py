import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------- LOAD DATA -------------------
@st.cache_data
def load_data():
    return pd.read_csv("spotify_history.csv")

df = load_data()

# ------------------- APP TITLE -------------------
st.title("🎵 Spotify Dashboard")
st.markdown("Explore insights from your Spotify listening history")

# ------------------- PREVIEW -------------------
st.subheader("Preview of Dataset")
st.dataframe(df.head())

# ------------------- SIDEBAR FILTERS -------------------
st.sidebar.header("Filters")

# Artist filter
if "artist_name" in df.columns:
    artists = df["artist_name"].dropna().unique()
    artist_filter = st.sidebar.multiselect("Select Artist(s)", artists)
    if artist_filter:
        df = df[df["artist_name"].isin(artist_filter)]

# Track filter
if "track_name" in df.columns:
    tracks = df["track_name"].dropna().unique()
    track_filter = st.sidebar.multiselect("Select Track(s)", tracks)
    if track_filter:
        df = df[df["track_name"].isin(track_filter)]

# Date filter
if "end_time" in df.columns:
    df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")
    min_date = df["end_time"].min().date()
    max_date = df["end_time"].max().date()

    date_filter = st.sidebar.date_input(
        "Select Date Range",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

    if len(date_filter) == 2:
        start_date, end_date = date_filter
        df = df[(df["end_time"].dt.date >= start_date) & (df["end_time"].dt.date <= end_date)]

# ------------------- VISUALIZATIONS -------------------

# Top Artists
if "artist_name" in df.columns:
    st.subheader("Top Artists")
    artist_count = df["artist_name"].value_counts().head(10)
    fig1 = px.bar(artist_count, x=artist_count.index, y=artist_count.values,
                  title="Top 10 Artists")
    st.plotly_chart(fig1)

# Top Tracks
if "track_name" in df.columns:
    st.subheader("Top Tracks")
    track_count = df["track_name"].value_counts().head(10)
    fig2 = px.bar(track_count, x=track_count.index, y=track_count.values,
                  title="Top 10 Tracks")
    st.plotly_chart(fig2)

# Listening Over Time
if "end_time" in df.columns:
    st.subheader("Listening Activity Over Time")
    time_series = df.groupby(df["end_time"].dt.date).size()
    fig3 = px.line(time_series, x=time_series.index, y=time_series.values,
                   title="Songs Played Over Time")
    st.plotly_chart(fig3)

st.success("✅ Dashboard Loaded Successfully")
