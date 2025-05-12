# utils/filters.py
import streamlit as st
from utils.database import load_coca_view
from utils.layout import UI_TEXT

@st.cache_data(ttl=600)
def load_unique_filters(df, column_name):
    return sorted(df[column_name].dropna().unique())


def set_filters_to_default():
    ss = st.session_state
    df = load_coca_view()

    ss['filter.disabled'] = False

    ss['province_list'] = ["All"] + sorted(df['province'].dropna().unique())
    ss['district_list'] = ["All"] + sorted(df['district_municipality'].dropna().unique())
    ss['indicator_list'] = ["All"] + sorted(df['indicator'].dropna().unique())
    ss['sub_indicator_list'] = ["All"] + sorted(df['sub_indicator'].dropna().unique())
    ss['sub_sub_indicator_list'] = ["All"] + sorted(df['sub_sub_indicator'].dropna().unique())


    ss["filter.province"] = "All"
    ss["filter.district"] = "All"
    ss["filter.indicator"] = "All"
    ss["filter.sub_indicator"] = "All"
    ss["filter.sub_sub_indicator"] = "All"


def render_sidebar_filters():
    df = load_coca_view()
    ss = st.session_state

    if "filter.province" not in ss:
        set_filters_to_default()

    st.sidebar.header("🔎 Filter Data")

    province = st.sidebar.selectbox("Province", ss['province_list'], key="filter.province")
    district = st.sidebar.selectbox("District Municipality", ss['district_list'], key="filter.district")
    indicator = st.sidebar.selectbox("Indicator", ss['indicator_list'], key="filter.indicator")

    # Cascading: sub_indicator depends on indicator
    if indicator != "All":
        sub_df = df[df["indicator"] == indicator]
        sub_indicator_list = ["All"] + sorted(sub_df["sub_indicator"].dropna().unique())
    else:
        sub_indicator_list = ss['sub_indicator_list']

    sub_indicator = st.sidebar.selectbox("Sub-Indicator", sub_indicator_list, key="filter.sub_indicator")

    if sub_indicator != "All":
        sub_sub_df = df[df["sub_indicator"] == sub_indicator]
        sub_sub_indicator_list = ["All"] + sorted(sub_sub_df["sub_sub_indicator"].dropna().unique())
    else:
        sub_sub_indicator_list = ss['sub_sub_indicator_list']

    sub_sub_indicator = st.sidebar.selectbox("Sub-Sub Indicator", sub_sub_indicator_list, key="filter.sub_sub_indicator")

    # Reset button
    st.sidebar.button(
        UI_TEXT["reset_button"],
        help=UI_TEXT["reset_tooltip"],
        on_click=set_filters_to_default
    )
    st.sidebar.divider()

    # Apply filters
    if ss["filter.province"] != "All":
        df = df[df['province'] == ss["filter.province"]]
    if ss["filter.district"] != "All":
        df = df[df['district_municipality'] == ss["filter.district"]]
    if ss["filter.indicator"] != "All":
        df = df[df['indicator'] == ss["filter.indicator"]]
    if ss["filter.sub_indicator"] != "All":
        df = df[df['sub_indicator'] == ss["filter.sub_indicator"]]
    if ss["filter.sub_sub_indicator"] != "All":
        df = df[df['sub_sub_indicator'] == ss["filter.sub_sub_indicator"]]

    return df
