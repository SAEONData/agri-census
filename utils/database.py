import os
from sqlalchemy import create_engine
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import text
import geopandas as gpd
import streamlit as st
import plotly.express as px


load_dotenv()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASS = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST")
DB_PORT = os.getenv("POSTGRES_PORT")
DB_NAME = os.getenv("POSTGRES_DB")

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

@st.cache_data(ttl=600)
def load_coca_view(province=None, district=None, indicator=None, sub_indicator=None):
    """
    Load data from the materialized view with optional filtering.
    Returns filtered pandas DataFrame.
    """
    conditions = []
    params = {}

    if province:
        conditions.append("province = ANY(:province)")
        params["province"] = province

    if district:
        conditions.append("district_municipality = ANY(:district)")
        params["district"] = district

    if indicator:
        conditions.append("indicator = :indicator")
        params["indicator"] = indicator

    if sub_indicator:
        conditions.append("sub_indicator = :sub_indicator")
        params["sub_indicator"] = sub_indicator

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT 
            province,
            district_municipality,
            census_region,
            indicator,
            sub_indicator,
            sub_indicator_number,
            sub_sub_indicator,
            unit,
            y2007,
            y2017,
            farming_units
        FROM public.coca_agriculture_with_boundaries
        {where_clause}
    """

    return pd.read_sql(text(query), engine, params=params)

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


@st.cache_data(ttl=3600)
def get_distinct_indicators(column):
    query = f"SELECT DISTINCT {column} FROM public.coca_agriculture_with_boundaries WHERE {column} IS NOT NULL"
    df = pd.read_sql(query, engine)
    return sorted(df[column].dropna().unique())


@st.cache_data(ttl=3600)
def load_spatial_query(query: str, params: dict = None, geom_col: str = "geometry") -> gpd.GeoDataFrame:
    """
    Loads a spatial query using GeoPandas from PostGIS.

    Args:
        query (str): SQL query string with spatial column included.
        params (dict, optional): SQL parameters to bind.
        geom_col (str): Name of the geometry column in the result.

    Returns:
        gpd.GeoDataFrame: Geo-enabled DataFrame for mapping.
    """
    try:
        gdf = gpd.read_postgis(query, con=engine, params=params, geom_col=geom_col)
        return gdf
    except Exception as e:
        print(f"[ERROR] Spatial query failed: {e}")
        return gpd.GeoDataFrame()


@st.cache_data(ttl=3600)
def farming_units_by_prov(province=None, district=None, indicator=None, sub_indicator=None):
    """
    Aggregate farming_units by province based on optional filters.
    Returns a pandas DataFrame with 'province', 'farming_units'.
    """
    conditions = []
    params = {}

    if province:
        conditions.append("province = ANY(:province)")
        params["province"] = province

    if district:
        conditions.append("district_municipality = ANY(:district)")
        params["district"] = district

    if indicator:
        conditions.append("indicator = :indicator")
        params["indicator"] = indicator

    if sub_indicator:
        conditions.append("sub_indicator = :sub_indicator")
        params["sub_indicator"] = sub_indicator

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT province, SUM(farming_units) AS farming_units
        FROM public.coca_agriculture_with_boundaries
        {where_clause}
        GROUP BY province
    """

    return pd.read_sql(text(query), engine, params=params)




@st.cache_data(ttl=3600)
def farming_units_by_district(province=None, district=None, indicator=None, sub_indicator=None):
    """
    Aggregate farming_units by district_municipality based on optional filters.
    Returns a DataFrame with 'district_municipality', 'farming_units'.
    """
    conditions = []
    params = {}

    if province:
        conditions.append("province = ANY(:province)")
        params["province"] = province

    if district:
        conditions.append("district_municipality = ANY(:district)")
        params["district"] = district

    if indicator:
        conditions.append("indicator = :indicator")
        params["indicator"] = indicator

    if sub_indicator:
        conditions.append("sub_indicator = :sub_indicator")
        params["sub_indicator"] = sub_indicator

    where_clause = "WHERE " + " AND ".join(conditions) if conditions else ""

    query = f"""
        SELECT district_municipality, SUM(farming_units) AS farming_units
        FROM public.coca_agriculture_with_boundaries
        {where_clause}
        GROUP BY district_municipality
    """

    return pd.read_sql(text(query), engine, params=params)

