# utils/filters.py
import streamlit as st
from utils.database import load_coca_view

@st.cache_data(ttl=600)
def load_unique_filters(df, column_name):
    return sorted(df[column_name].dropna().unique())

def render_sidebar_filters():
    """Render all sidebar filters and return filtered dataset."""
    df = load_coca_view()

    st.sidebar.header("🔎 Filter Data")

    provinces = load_unique_filters(df, "province")
    province = st.sidebar.selectbox("Province", ["All"] + provinces)

    districts = load_unique_filters(df, "district_municipality")
    district = st.sidebar.selectbox("District Municipality", ["All"] + districts)

    indicators = load_unique_filters(df, "indicator")
    indicator = st.sidebar.selectbox("Indicator", ["All"] + indicators)

    sub_indicators = load_unique_filters(df, "sub_indicator")
    sub_indicator = st.sidebar.selectbox("Sub-Indicator", ["All"] + sub_indicators)

    sub_sub_indicators = load_unique_filters(df, "sub_sub_indicator")
    sub_sub_indicator = st.sidebar.selectbox("Sub-Sub Indicator", ["All"] + sub_sub_indicators)

    # Filter the dataset based on selected values
    if province != "All":
        df = df[df["province"] == province]
    if district != "All":
        df = df[df["district_municipality"] == district]
    if indicator != "All":
        df = df[df["indicator"] == indicator]
    if sub_indicator != "All":
        df = df[df["sub_indicator"] == sub_indicator]
    if sub_sub_indicator != "All":
        df = df[df["sub_sub_indicator"] == sub_sub_indicator]

    return df
