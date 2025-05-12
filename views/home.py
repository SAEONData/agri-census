# views/home.py

import streamlit as st
from utils.database import get_summary_stats, get_top_indicators, get_province_distribution
from utils.layout import PAGE_HELP_TEXT
from utils.colors import get_indicator_colors
import plotly.express as px

def show():
    # Header logos
    col1, col2 = st.columns([1, 1])
    with col1:
        st.image("images/saeon_logo.png", width=180)
    with col2:
        st.image("images/statssa_logo.png", width=180)

    st.title("2017 Agricultural Census Dashboard")
    st.subheader("A decision-support tool by SAEON/NRF")
    st.markdown("---")
    st.markdown("This dashboard provides insights into the 2017 Agricultural Census data, focusing on farm land census. The data is sourced from the Stats SA 2017 Agricultural Census and is made available through the SAEON/NRF platform.")
    st.markdown("---")
    
    st.markdown("### 📈 CoCA 2017 at a Glance")
    st.markdown("The following metrics provide a snapshot of the 2017 Agricultural Census data.")
    
    stats = get_summary_stats()
    col1, col2, col3 = st.columns(3)
    col1.metric("📄 Total Farms Recorded", f"{stats.record_count:,}")
    col2.metric("🗺️ Provinces Covered", stats.province_count)
    col3.metric("📊 Farm Indicators", stats.indicator_count)

    st.markdown("---")
    st.markdown("#### 🔎 Top 5 Indicators")
    top_indicators = get_top_indicators()
    indicator_colors = get_indicator_colors()
    
    fig1 = px.bar(
        top_indicators,
        x="count",
        y="indicator",
        orientation="h",
        labels={"indicator": "Indicator", "count": "Records"},
        color="indicator",
        color_discrete_map=indicator_colors,
        height=400
    )

    fig1.update_layout(
            showlegend=False,
            margin=dict(l=100, r=40, t=40, b=40)
        )
    
    st.plotly_chart(fig1, use_container_width=True)

    # Province Distribution Chart
    st.markdown("#### 🗺️ Distribution by Province")
    province_dist = get_province_distribution()
    fig2 = px.pie(
        province_dist, names="province", values="count",
        title="", hole=0.4
    )
    st.plotly_chart(fig2, use_container_width=True)
    
    # Contextual intro and links
    st.markdown(PAGE_HELP_TEXT["home"])
    st.markdown("---")
    st.markdown(PAGE_HELP_TEXT["home_links"])

    
