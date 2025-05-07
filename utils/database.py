# utils/database.py
import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
import streamlit as st
import plotly.express as px


load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

# SQLAlchemy engine
DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@st.cache_data(ttl=600)
def load_coca_view():
    """Load data from the materialized view for use in all modules."""
    query = "SELECT * FROM public.coca_agriculture_with_boundaries"
    return pd.read_sql(query, engine)

@st.cache_data(ttl=600)
def get_indicator_list():
    """Get list of available indicators for sidebar filters."""
    query = "SELECT DISTINCT indicator FROM public.coca_agriculture_with_boundaries ORDER BY indicator;"
    return pd.read_sql(query, engine)['indicator'].dropna().tolist()

@st.cache_data(ttl=600)
def get_region_list():
    """Get list of available regions for sidebar filters."""
    query = "SELECT DISTINCT region FROM public.coca_agriculture_with_boundaries ORDER BY region;"
    return pd.read_sql(query, engine)['region'].dropna().tolist()


@st.cache_data(ttl=600)
def get_summary_stats():
    """Load only aggregated data needed for the home page metrics."""
    query = """
        SELECT
            COUNT(*) AS record_count,
            COUNT(DISTINCT province) AS province_count,
            COUNT(DISTINCT indicator) AS indicator_count
        FROM public.coca_agriculture_with_boundaries;
    """
    return pd.read_sql(query, engine).iloc[0]


@st.cache_data(ttl=600)
def get_top_indicators():
    query = """
        SELECT indicator, COUNT(*) AS count
        FROM public.coca_agriculture_with_boundaries
        GROUP BY indicator
        ORDER BY count DESC
        LIMIT 5;
    """
    return pd.read_sql(query, engine)

top_indicators = get_top_indicators()
fig = px.bar(top_indicators, x="count", y="indicator", orientation="h",
             title="Top 5 Indicators",
             labels={"count": "Records", "indicator": "Indicator"},
             height=300)
st.plotly_chart(fig, use_container_width=True)


@st.cache_data(ttl=600)
def get_province_distribution():
    query = """
        SELECT province, COUNT(*) AS count
        FROM public.coca_agriculture_with_boundaries
        GROUP BY province
        ORDER BY count DESC;
    """
    return pd.read_sql(query, engine)

province_dist = get_province_distribution()
fig = px.pie(province_dist, names="province", values="count",
             title="Record Distribution by Province",
             hole=0.4)
st.plotly_chart(fig, use_container_width=True)

