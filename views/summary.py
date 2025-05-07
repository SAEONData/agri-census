# views/summary.py

import streamlit as st
from utils.filters import render_sidebar_filters
from utils.layout import PAGE_HELP_TEXT
import plotly.express as px

def show():
    st.title("📊 Summary Dashboard")
    st.markdown(PAGE_HELP_TEXT["summary"])

    # Load filtered dataset from sidebar
    df = render_sidebar_filters()

    if df.empty:
        st.warning("No data matches your current filters.")
        return

    # Metric summary section
    st.markdown("### 🧮 Key Stats")

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Records", f"{len(df):,}")
    col2.metric("🧑‍🌾 Unique Regions", df["census_region"].nunique())
    col3.metric("📌 Indicators", df["indicator"].nunique())

    # Optional: show top sub_indicators by count
    st.markdown("### 🔍 Top 5 Sub-Indicators (by Count)")
    top_sub = (
        df.groupby("sub_indicator")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="count")
        .head(5)
    )

    fig = px.bar(
        top_sub, x="count", y="sub_indicator", orientation="h",
        labels={"sub_indicator": "Sub-Indicator", "count": "Records"},
        height=300
    )
    st.plotly_chart(fig, use_container_width=True)

    # Optional table preview
    with st.expander("🔎 Preview Filtered Records", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)
