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

    ss['province_list'] = sorted(df['province'].dropna().unique())
    ss['district_list'] = sorted(df['district_municipality'].dropna().unique())
    ss['indicator_list'] = sorted(df['indicator'].dropna().unique())
    ss['sub_indicator_list'] = sorted(df['sub_indicator'].dropna().unique())
    ss['sub_sub_indicator_list'] = sorted(df['sub_sub_indicator'].dropna().unique())

    ss["filter.province"] = []
    ss["filter.district"] = []
    ss["filter.indicator"] = None
    ss["filter.sub_indicator"] = None
    ss["filter.sub_sub_indicator"] = None


def render_sidebar_filters():
    df = load_coca_view()
    ss = st.session_state

    if "filter.province" not in ss:
        set_filters_to_default()

    st.sidebar.header("🔎 Filter Data")

    # Multi-select: Province & District
    province = st.sidebar.multiselect("Province", ss['province_list'][1:], key="filter.province")
    district = st.sidebar.multiselect("District Municipality", ss['district_list'][1:], key="filter.district")

    # Single-select: Indicator
    indicator = st.sidebar.selectbox("Indicator", [None] + ss['indicator_list'], format_func=lambda x: "All" if x is None else x, key="filter.indicator")

    # Cascading sub_indicator
    if indicator:
        sub_df = df[df["indicator"] == indicator]
        sub_indicator_list = ["All"] + sorted(sub_df["sub_indicator"].dropna().unique())
    else:
        sub_indicator_list = ss['sub_indicator_list']

    sub_indicator = st.sidebar.selectbox("Sub-Indicator", [None] + sub_indicator_list, format_func=lambda x: "All" if x is None else x, key="filter.sub_indicator")

    # Cascading sub_sub_indicator
    if sub_indicator != "All":
        sub_sub_df = df[df["sub_indicator"] == sub_indicator]
        sub_sub_indicator_list = ["All"] + sorted(sub_sub_df["sub_sub_indicator"].dropna().unique())
    else:
        sub_sub_indicator_list = ss['sub_sub_indicator_list']

    sub_sub_indicator = st.sidebar.selectbox("Sub-Sub Indicator", [None] + sub_sub_indicator_list, format_func=lambda x: "All" if x is None else x, key="filter.sub_sub_indicator")

    # Reset button
    st.sidebar.button(
        UI_TEXT["reset_button"],
        help=UI_TEXT["reset_tooltip"],
        on_click=set_filters_to_default
    )
    st.sidebar.divider()

    # --- Apply Filters ---
    if ss.get("filter.province"):
        df = df[df['province'].isin(ss["filter.province"])]

    if ss.get("filter.district"):
        df = df[df['district_municipality'].isin(ss["filter.district"])]

    if ss.get("filter.indicator"):
        df = df[df['indicator'] == ss["filter.indicator"]]

    if ss.get("filter.sub_indicator"):
        df = df[df['sub_indicator'] == ss["filter.sub_indicator"]]

    if ss.get("filter.sub_sub_indicator"):
        df = df[df['sub_sub_indicator'] == ss["filter.sub_sub_indicator"]]

    return df


def get_filter_summary(df):
    ss = st.session_state
    filters = []

    if ss.get("filter.province"):
        filters.append(", ".join(ss["filter.province"]))

    if ss.get("filter.indicator"):
        filters.append(ss["filter.indicator"])

    if ss.get("filter.sub_indicator"):
        filters.append(ss["filter.sub_indicator"])

    filter_text = " > ".join(filters) if filters else "all provinces and indicators"
    return f"**Showing {len(df):,} records filtered by:** {filter_text}"


