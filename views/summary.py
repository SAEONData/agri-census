# views/summary.py

import streamlit as st
import plotly.express as px
from utils.filters import render_sidebar_filters
from utils.layout import PAGE_HELP_TEXT
from utils.colors import get_sub_indicator_colors

def show():
    st.title("📊 Summary")
    st.markdown(PAGE_HELP_TEXT["summary"])

    # Load filtered dataset from sidebar
    df = render_sidebar_filters()

    if df.empty:
        st.warning("No data matches your current filters.")
        return

    st.markdown("---")
    st.markdown("### 🧮 Key Stats")

    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Total Farms", f"{len(df):,}")
    col2.metric("🧑‍🌾 Regions", df["census_region"].nunique())
    col3.metric("📌 Indicators", df["indicator"].nunique())

    st.markdown("---")
    st.markdown("### 🔍 Top 10 Sub-Indicators (by Count)")

    top_sub = (
        df.groupby("sub_indicator")
        .size()
        .sort_values(ascending=False)
        .reset_index(name="count")
        .head(10)
    )

    sub_indicator_colors = get_sub_indicator_colors()

    fig = px.bar(
    top_sub,
    x="count",
    y="sub_indicator",
    orientation="h",
    labels={"sub_indicator": "Sub-Indicator", "count": "Records"},
    color="sub_indicator",
    color_discrete_map=sub_indicator_colors,
    height=600,
)

    fig.update_layout(
        showlegend=False,
        margin=dict(l=100, r=40, t=40, b=40)
    )
 
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    with st.expander("🔎 Preview Filtered Records", expanded=False):
        st.dataframe(df.head(20), use_container_width=True)
